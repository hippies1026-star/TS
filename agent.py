import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from finance_tools import TOOLS, execute_tool

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

SYSTEM_PROMPT = """
너는 초기 스타트업을 위한 생존기반 AI CFO Agent인 TreaSurv다.
목표는 단기 금융수익 극대화가 아니라 기업이 사업계획을 수행하면서도 생존에 필요한 현금을 보호하도록 의사결정을 돕는 것이다.

판단 원칙:
1. 숫자를 임의 계산하지 말고 등록된 Tool을 사용한다.
2. Burn Rate와 Runway를 먼저 확인한다.
3. 스트레스 시나리오를 반영한 Survival Floor를 계산한다.
4. Survival Floor 이하 현금은 운용 대상으로 보지 않는다.
5. 사업계획이 관련된 질문이면 forecast tool로 계획 반영 현금흐름을 확인한다.
6. 최대 운용가능자금 이후에만 사용자의 운용성향을 적용한다.
7. 매우 적극적인 운용성향이라도 Survival Floor를 침범하지 않는다.
8. 제공된 데이터와 가정을 구분하고, 확인되지 않은 금융상품·수익률·시장정보를 사실처럼 만들지 않는다.

답변은 경영자가 바로 판단할 수 있게 다음 순서로 간결하게 작성한다.
- 결론
- 핵심 숫자
- 판단 근거
- 주요 위험요인
- 다음 액션
"""


def _get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


def analyze_company(user_prompt: str):
    client = _get_client()
    if client is None:
        return (
            "AI 분석을 실행하려면 프로젝트의 `.env`에 `GROQ_API_KEY`가 필요합니다. "
            "재무 계산과 Forecast 기능은 API 키 없이도 정상 동작합니다."
        )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    try:
        for _ in range(12):
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.1,
            )

            message = response.choices[0].message
            messages.append(message)

            if not message.tool_calls:
                return message.content or "분석 결과를 생성하지 못했습니다."

            for tool_call in message.tool_calls:
                try:
                    arguments = json.loads(tool_call.function.arguments or "{}")
                    result = execute_tool(tool_call.function.name, arguments)
                except Exception as exc:
                    result = {"error": f"Tool 실행 실패: {exc}"}

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

        return "분석 단계가 너무 길어 중단되었습니다. 질문 범위를 조금 좁혀 다시 시도해 주세요."
    except Exception as exc:
        return (
            "AI CFO 연결에 실패했습니다. 재무 계산 결과는 유지됩니다. "
            f"API/모델 설정을 확인해 주세요. ({type(exc).__name__})"
        )
