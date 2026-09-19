import streamlit as st


def apply_global_styles():

    st.html(
        """
        <style>

        /* ==================================================
           STREAMLIT DEFAULT UI
        ================================================== */

        /* Keep Streamlit's sidebar collapse / expand control available. */
        [data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu,
        footer,
        .stDeployButton {
            display: none !important;
            visibility: hidden !important;
        }

        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999999 !important;
        }


        /* ==================================================
           GLOBAL
        ================================================== */

        :root {
            --purple-main: #6D28D9;
            --purple-soft: #8B5CF6;
            --purple-light: #F4F0FC;

            --text-main: #292232;
            --text-sub: #83798E;
            --text-light: #A49BAE;

            --border: #ECE8F2;
            --background: #F7F7FA;
            --card: #FFFFFF;
        }

        html,
        body,
        .stApp {
            font-family:
                Inter,
                Pretendard,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        html {
            scroll-behavior: smooth;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 95% 0%,
                    rgba(124, 58, 237, 0.055),
                    transparent 23%
                ),
                var(--background);
        }

        .block-container {
            max-width: 1320px !important;

            padding-top: 2.2rem !important;
            padding-left: 2.6rem !important;
            padding-right: 2.6rem !important;
            padding-bottom: 4rem !important;

            animation:
                pageFade .24s ease-out;
        }

        @keyframes pageFade {

            from {
                opacity: 0;
                transform: translateY(5px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }


        /* ==================================================
           SIDEBAR
        ================================================== */

        section[data-testid="stSidebar"] {
            background: #FFFFFF !important;

            border-right:
                1px solid var(--border);

            box-shadow:
                6px 0 25px
                rgba(41, 28, 59, 0.025);
        }

        section[data-testid="stSidebar"]
        > div {

            padding-top:
                1.4rem !important;

            padding-left:
                .75rem !important;

            padding-right:
                .75rem !important;
        }


        /* Brand */

        .brand {
            display: flex;
            align-items: center;

            gap: 11px;

            padding:
                5px 7px 18px 7px;
        }

        .brand-logo {
            width: 43px;
            height: 43px;

            display: flex;
            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 13px;

            background:
                linear-gradient(
                    135deg,
                    #6828D6,
                    #8B5CF6
                );

            color: white;

            font-size: 16px;
            font-weight: 850;
            letter-spacing: -.6px;

            box-shadow:
                0 9px 22px
                rgba(109, 40, 217, .18);
        }

        .brand-name {
            color: #2B2433;

            font-size: 19px;
            font-weight: 820;

            line-height: 1;
            letter-spacing: -.55px;
        }

        .brand-sub {
            margin-top: 5px;

            color: #AAA1B4;

            font-size: 9.5px;
            font-weight: 530;
        }


        /* Company */

        .company-box {
            display: flex;
            align-items: center;

            gap: 10px;

            padding: 11px;

            margin:
                2px 2px 12px 2px;

            border-radius: 14px;

            background: #F7F5FA;

            transition:
                background .16s ease,
                transform .16s ease;
        }

        .company-box:hover {
            background: #F3F0F8;
        }

        .company-icon {
            width: 34px;
            height: 34px;

            display: flex;
            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 10px;

            background: #EDE6FA;

            color: var(--purple-main);

            font-weight: 820;
            font-size: 13px;
        }

        .company-name {
            color: #3A3242;

            font-size: 12.5px;
            font-weight: 720;
        }

        .company-type {
            color: #AAA1B2;

            margin-top: 2px;

            font-size: 9.5px;
        }


        /* User */

        .sidebar-user {
            display: flex;
            align-items: center;

            gap: 9px;

            padding:
                8px 5px;
        }

        .user-avatar {
            width: 33px;
            height: 33px;

            display: flex;
            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            border-radius: 50%;

            background: #EEE8F8;

            color: var(--purple-main);

            font-size: 12px;
            font-weight: 800;
        }

        .user-name {
            color: #3A3242;

            font-size: 11.5px;
            font-weight: 720;
        }

        .user-role {
            color: #AAA1B1;

            margin-top: 2px;

            font-size: 9px;
        }


        /* ==================================================
           LOGIN
        ================================================== */

        .login-wrapper {
            text-align: center;

            padding-top: 8vh;
            padding-bottom: 28px;
        }

        .login-logo {
            width: 65px;
            height: 65px;

            margin:
                0 auto 16px auto;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 19px;

            background:
                linear-gradient(
                    135deg,
                    #6828D6,
                    #8B5CF6
                );

            color: white;

            font-size: 21px;
            font-weight: 850;

            box-shadow:
                0 13px 30px
                rgba(109, 40, 217, .23);
        }

        .login-brand {
            color: #292131;

            font-size: 30px;
            font-weight: 850;

            letter-spacing: -1px;
        }

        .login-tagline {
            margin-top: 6px;

            color: #9B91A5;

            font-size: 12px;
        }

        .login-title {
            color: #2B2432;

            font-size: 21px;
            font-weight: 800;

            margin-bottom: 5px;
        }

        .login-description {
            color: #958B9F;

            font-size: 12px;

            margin-bottom: 22px;
        }

        .login-divider {
            display: flex;
            align-items: center;

            gap: 10px;

            margin: 22px 0 16px;
        }

        .login-divider span {
            height: 1px;
            flex: 1;

            background: #ECE8F1;
        }

        .login-divider p {
            margin: 0;

            color: #AAA1B3;

            font-size: 10px;
        }

        .demo-notice {
            margin-top: 16px;

            text-align: center;

            color: #A59CAD;

            font-size: 10px;
        }


        /* ==================================================
           TITLES
        ================================================== */

        .page-title {
            color: #2B2433;

            font-size: 30px;
            font-weight: 830;

            letter-spacing: -1.05px;
            line-height: 1.25;
        }

        .page-subtitle {
            color: #92889D;

            margin-top: 6px;
            margin-bottom: 28px;

            font-size: 13px;
        }

        .section-title {
            color: #342C3D;

            margin-top: 30px;
            margin-bottom: 14px;

            font-size: 18px;
            font-weight: 770;

            letter-spacing: -.4px;
        }


        /* ==================================================
           CONTAINERS / CARDS
        ================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {

            border:
                1px solid var(--border) !important;

            border-radius:
                18px !important;

            background:
                rgba(255,255,255,.96) !important;

            box-shadow:
                0 5px 18px
                rgba(55, 38, 76, .03) !important;

            transition:
                transform .15s ease,
                box-shadow .15s ease,
                border-color .15s ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {

            border-color:
                #E1DAEA !important;

            box-shadow:
                0 8px 24px
                rgba(55, 38, 76, .045) !important;
        }


        .card {
            min-height: 128px;

            padding: 20px;

            border:
                1px solid var(--border);

            border-radius: 18px;

            background: #FFFFFF;

            box-shadow:
                0 5px 18px
                rgba(52, 34, 75, .035);

            transition:
                transform .16s ease,
                box-shadow .16s ease;
        }

        .card:hover {
            transform:
                translateY(-2px);

            box-shadow:
                0 10px 28px
                rgba(52, 34, 75, .055);
        }

        .card-label {
            color: #968C9F;

            font-size: 10.5px;
            font-weight: 720;

            letter-spacing: .35px;
        }

        .card-value {
            color: #302837;

            margin-top: 9px;

            font-size: 25px;
            font-weight: 830;

            letter-spacing: -.65px;
        }

        .card-note {
            color: #AAA2B0;

            margin-top: 9px;

            font-size: 10.5px;
        }

        .purple {
            color:
                var(--purple-main);
        }


        /* ==================================================
           STREAMLIT METRICS
        ================================================== */

        [data-testid="stMetric"] {

            padding: 19px;

            border:
                1px solid var(--border);

            border-radius: 18px;

            background: #FFFFFF;

            box-shadow:
                0 5px 18px
                rgba(52, 34, 75, .028);
        }

        [data-testid="stMetricLabel"] {
            color: #8F8599;
        }

        [data-testid="stMetricValue"] {

            color: #302837;

            font-weight: 800;
            letter-spacing: -.5px;
        }


        /* ==================================================
           BUTTON
        ================================================== */

        div.stButton > button {

            min-height: 43px;

            border:
                1px solid #E8E3EE !important;

            border-radius:
                12px !important;

            background:
                #FFFFFF !important;

            color:
                #504657 !important;

            font-size:
                12px !important;

            font-weight:
                650 !important;

            box-shadow: none !important;

            transition:
                all .14s ease;
        }

        div.stButton > button:hover {

            border-color:
                #DCCFF1 !important;

            background:
                #F8F5FC !important;

            color:
                var(--purple-main) !important;
        }


        div.stButton > button[kind="primary"] {

            border:
                none !important;

            background:
                linear-gradient(
                    135deg,
                    #6D28D9,
                    #7C3AED
                ) !important;

            color:
                white !important;

            box-shadow:
                0 8px 20px
                rgba(109,40,217,.17) !important;
        }

        div.stButton > button[kind="primary"]:hover {

            background:
                linear-gradient(
                    135deg,
                    #6122C5,
                    #7131DC
                ) !important;

            color:
                white !important;

            transform:
                translateY(-1px);
        }


        /* ==================================================
           INPUTS
        ================================================== */

        [data-testid="stWidgetLabel"] p {

            color:
                #655C6C !important;

            font-size:
                11.5px !important;

            font-weight:
                620 !important;
        }

        input,
        textarea {

            border-radius:
                11px !important;
        }

        [data-baseweb="select"] > div {

            border-radius:
                11px !important;
        }


        /* ==================================================
           CHAT
        ================================================== */

        [data-testid="stChatMessage"] {

            border-radius:
                16px;

            animation:
                chatFade .18s ease;
        }

        @keyframes chatFade {

            from {
                opacity: 0;
                transform: translateY(3px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        [data-testid="stChatInput"] {

            border-radius:
                15px;
        }


        /* ==================================================
           ALERTS
        ================================================== */

        [data-testid="stAlert"] {

            border-radius:
                13px;

            font-size:
                12px;
        }


        /* ==================================================
           DATAFRAME
        ================================================== */

        [data-testid="stDataFrame"] {

            overflow: hidden;

            border:
                1px solid var(--border);

            border-radius:
                15px;
        }


        /* ==================================================
           EXPANDERS
        ================================================== */

        [data-testid="stExpander"] {

            border:
                1px solid var(--border) !important;

            border-radius:
                14px !important;

            background:
                #FFFFFF;
        }


        /* ==================================================
           CHART
        ================================================== */

        [data-testid="stPlotlyChart"] {

            overflow: hidden;

            border:
                1px solid var(--border);

            border-radius:
                18px;

            background: #FFFFFF;

            padding: 5px;
        }


        /* ==================================================
           STATUS BADGES
        ================================================== */

        .status-connected {
            display: inline-flex;
            align-items: center;

            padding:
                5px 9px;

            border-radius:
                999px;

            background:
                #ECF8F1;

            color:
                #278654;

            font-size:
                9.5px;

            font-weight:
                720;
        }

        .status-connected:before {

            content: "";

            width: 6px;
            height: 6px;

            margin-right: 5px;

            border-radius: 50%;

            background:
                #36B66D;
        }

        .status-demo {
            display: inline-block;

            padding:
                5px 9px;

            border-radius:
                999px;

            background:
                #F1EBFA;

            color:
                var(--purple-main);

            font-size:
                9.5px;

            font-weight:
                720;
        }


        /* ==================================================
           FOOTER
        ================================================== */

        .global-footer {

            margin-top: 55px;

            padding:
                25px 0 10px 0;

            border-top:
                1px solid #E9E5ED;

            text-align: center;

            color:
                #A29AAA;

            font-size:
                9.5px;

            line-height:
                1.8;
        }

        .global-footer strong {

            color:
                #706776;

            font-weight:
                650;
        }

        .footer-meta {
            margin-top: 3px;
        }

        .footer-links {

            display: flex;
            justify-content: center;

            gap: 7px;

            margin-top: 8px;

            color:
                #8F8597;
        }

        .footer-links span {
            color:
                #CDC7D1;
        }

        .footer-copy {
            margin-top: 7px;
        }

        .footer-prototype {

            margin-top: 9px;

            color:
                #B5AEBB;
        }


        /* ==================================================
           PROTOTYPE NOTICE
        ================================================== */

        .prototype-notice {

            margin-top: 28px;

            padding:
                10px 13px;

            border-radius:
                11px;

            background:
                #F3F0F7;

            color:
                #9F95A9;

            text-align:
                center;

            font-size:
                9.5px;
        }


        /* ==================================================
           RESPONSIVE
        ================================================== */

        @media (
            max-width: 900px
        ) {

            .block-container {

                padding-left:
                    1rem !important;

                padding-right:
                    1rem !important;
            }

            .page-title {
                font-size: 25px;
            }

        }

        </style>
        """
    )