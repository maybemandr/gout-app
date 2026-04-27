import streamlit as st

# ================= 页面基础设置 =================
st.set_page_config(page_title="多指南痛风智能决策系统", page_icon="⚕️", layout="centered")

# ================= 顶部 Logo 与标题区 =================
# 将页面分为左右两列，比例大概是 1:5（左边窄放图片，右边宽放文字）
col_logo, col_title = st.columns([1, 5])

with col_logo:
    # 加载你的 Logo 图片（请确保你已经在 GitHub 上传了这张名为 logo.png 的图片）
    # 如果暂时还没上传图片，系统会报错。你可以先把下面这行代码前面加个 # 注释掉
    st.image("logo.png", use_container_width=True)

with col_title:
    st.title("⚕️ 痛风及高尿酸血症中西医诊疗智能决策系统（2026）")
    st.markdown("<font color='#7f8c8d'>基于 2020-2024 中美权威指南及中西医结合指南构建</font>", unsafe_allow_html=True)
    st.markdown("<font color='#95a5a6' size='2'><i>© 2026 版权归属于澳门大学中药机制与质量全国重点实验室 QC 组。</i></font>", unsafe_allow_html=True)

st.divider()

# ================= 1. 输入区 =================
st.subheader("1. 基础指标与患者背景")
col1, col2 = st.columns(2)
with col1:
    sua = st.number_input("血尿酸 (SUA, μmol/L):", min_value=0.0, max_value=1500.0, value=520.0, step=10.0)
with col2:
    race_option = st.selectbox("种族/族裔背景:", ["亚裔 (如汉族、韩国等)", "非裔", "高加索裔/其他"])
    race_idx = ["亚裔 (如汉族、韩国等)", "非裔", "高加索裔/其他"].index(race_option)

st.subheader("2. 痛风发作频率与症状特征")
st.markdown("<font color='#c0392b'><b>▶ 西医分期与中医辨证依据 (可多选)：</b></font>", unsafe_allow_html=True)

cb_never = st.checkbox("从未发作过痛风 (无临床症状)")
cb_first = st.checkbox("首次痛风急性发作")
cb_infreq = st.checkbox("偶尔发作 (过去一年 < 2次)")
cb_freq = st.checkbox("频繁发作 (过去一年 ≥ 2次)")
cb_acute = st.checkbox("当前正处于急性发作期 (关节红肿热痛剧烈)")
cb_tophi = st.checkbox("查体可见皮下痛风石或影像学提示尿酸盐沉积性骨破坏")

st.markdown("<font color='#27ae60'><b>▶ 中医核心症候 (可多选)：</b></font>", unsafe_allow_html=True)
cb_cold = st.checkbox("关节冷痛，得热痛减，畏寒肢冷 (提示:寒湿)")
cb_damp = st.checkbox("肢体困重，纳呆食少，大便黏滞 (提示:湿浊/湿热)")
cb_def = st.checkbox("腰膝酸软，神疲乏力，夜尿频多 (提示:脾肾亏虚)")

st.subheader("3. 伴随合并症")
st.markdown("<font color='#2980b9'><b>▶ 合并症将显著影响西药选择与靶标 (可多选)：</b></font>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    cb_ckd = st.checkbox("慢性肾脏病 (CKD ≥ 3期)")
    cb_stone = st.checkbox("泌尿系统尿酸盐结石")
    cb_dm = st.checkbox("糖尿病")
with col4:
    cb_cvd = st.checkbox("心血管疾病史 (心衰、近期心梗等)")
    cb_gi = st.checkbox("消化道溃疡或活动性出血史")
    cb_htn = st.checkbox("高血压 / 脂代谢异常 / 肥胖")

st.divider()

# ================= 2. 逻辑推断与输出区 =================
if st.button("生成综合指南诊疗策略", type="primary"):
    
    # 合并症状态
    has_any_comorb = cb_ckd or cb_cvd or cb_stone or cb_dm or cb_htn

    # ---- 状态推断 ----
    clinical_state = ""
    if cb_never and not cb_tophi:
        clinical_state = "无症状高尿酸血症 (AHU)"
    elif cb_tophi:
        clinical_state = "慢性痛风性关节炎 (伴痛风石/骨破坏)"
    elif cb_acute:
        clinical_state = "痛风急性发作期"
    elif cb_freq or cb_infreq or cb_first:
        clinical_state = "痛风间歇期"
    else:
        clinical_state = "高尿酸血症/痛风状态未明确"

    # ================= 策略1: 2024 中国指南 =================
    cn_target = "&lt; 360 μmol/L"
    if cb_tophi or cb_ckd:
        cn_target = "&lt; 300 μmol/L"

    cn_ult_init = ""
    if clinical_state == "无症状高尿酸血症 (AHU)":
        if sua >= 540:
            cn_ult_init = "**建议启动降尿酸治疗 (ULT)**。因为单纯无症状患者血尿酸 ≥ 540 μmol/L。"
        elif sua >= 480 and has_any_comorb:
            cn_ult_init = "**建议启动降尿酸治疗 (ULT)**。因为伴有合并症且血尿酸 ≥ 480 μmol/L。"
        else:
            cn_ult_init = "暂不强制启动西药降尿酸，建议长期生活方式干预并密切监测。"
    else:
        if sua >= 480 or (sua >= 420 and (has_any_comorb or cb_freq or cb_tophi)):
            cn_ult_init = "**强烈建议启动或维持降尿酸治疗 (ULT)**。"
        else:
            cn_ult_init = "建议生活方式干预，若发作频繁或有合并症仍可考虑降尿酸治疗。"

    cn_meds = ""
    if cb_ckd:
        cn_meds += "• **CKD患者：** 推荐非布司他为一线用药(4-5期最大剂量40mg/d)，别嘌醇为二线。禁用苯溴马隆。\n"
    else:
        cn_meds += "• **降尿酸一线药物：** 非布司他、别嘌醇、苯溴马隆均可。若提示肾脏排泄不良，优选苯溴马隆。\n"
    if cb_cvd:
        cn_meds += "• **心血管合并症：** 痛风急性发作首选秋水仙碱，避免使用非甾体抗炎药(NSAIDs)。\n"
    if cb_gi:
        cn_meds += "• **消化道溃疡/出血：** 急性发作期避免使用非选择性NSAIDs，首选COX-2抑制剂或短期糖皮质激素。\n"
    if cb_dm:
        cn_meds += "• **糖尿病：** 若需使用激素抗炎，在严格控糖前提下，优先推荐关节腔内注射曲安奈德，优于全身用药。\n"

    # ================= 策略2: 2020 美国 ACR 指南 =================
    acr_target = "强烈推荐采用达标治疗，血尿酸靶标 **&lt; 6.0 mg/dL (约 360 μmol/L)**。"
    
    acr_ult_init = ""
    if cb_tophi or cb_freq:
        acr_ult_init = "**强烈推荐开启ULT**。（基于痛风石或频繁发作 ≥2次/年）。"
    elif cb_infreq:
        acr_ult_init = "**条件性推荐开启ULT**。（针对不频繁发作）。"
    elif cb_first:
        if cb_ckd or sua >= 540 or cb_stone:
            acr_ult_init = "**条件性推荐开启ULT**。（虽然首次发作，但伴有严重合并症或 SUA &gt; 540）。"
        else:
            acr_ult_init = "**条件性不推荐开启ULT**。（首次发作且无上述合并症）。"
    else:
        acr_ult_init = "**强烈建议不要开启ULT**。 (ACR不建议治疗无症状高尿酸血症)。"

    acr_meds = "• **一线降尿酸：** 强烈推荐**别嘌醇**为所有患者首选。\n"
    if race_idx in [0, 1]:
        acr_meds += "• **基因筛查：** 条件性推荐在亚裔和非裔人群开启别嘌醇前进行 **HLA-B*5801** 基因检测。\n"
    if cb_cvd:
         acr_meds += "• **心血管风险：** 对于有心血管病史的患者，条件性推荐将非布司他替换为其他降尿酸药物。\n"
    if not cb_never:
         acr_meds += "• **抗炎预防：** 强烈推荐开启ULT时，同步给予抗炎预防治疗至少 3-6 个月。\n"

    # ================= 策略3: 2023 中西医结合诊疗指南 =================
    tcm_syndrome = "证候未明确，请结合脉象与舌诊"
    tcm_rx = ""

    if cb_tophi:
        if cb_def:
            tcm_syndrome = "脾肾亏虚 伴 痰瘀痹阻"
            tcm_rx = "推荐：**济生肾气丸 合 参苓白术散** 配合化痰通络之品。"
        else:
            tcm_syndrome = "痰瘀痹阻证"
            tcm_rx = "治以化痰散结，活血通络。推荐：**上中下通用痛风方** 或 **双合汤**。"
    elif cb_acute:
        if cb_cold:
            tcm_syndrome = "寒湿痹阻证"
            tcm_rx = "治以温经散寒，祛湿通络。推荐：**桂枝附子汤** 或 **桂枝芍药知母汤**。"
        else:
            tcm_syndrome = "湿热毒蕴证"
            tcm_rx = "治以清热解毒，利湿化浊。推荐：**四妙散、当归拈痛汤**。"
    else:
        if cb_cold:
            tcm_syndrome = "寒湿痹阻证"
            tcm_rx = "治以温经散寒，祛湿通络。推荐：**桂枝附子汤** 或 **桂枝芍药知母汤**。"
        elif cb_damp:
            tcm_syndrome = "湿浊内蕴证"
            tcm_rx = "推荐：**平胃散 合 五苓散**。"
        elif cb_def:
            tcm_syndrome = "脾肾亏虚证"
            tcm_rx = "治以健脾益肾，燥湿化浊。推荐：**济生肾气丸 合 参苓白术散** 或 **黄葵胶囊**。"

    if not tcm_rx:
        tcm_rx = "未勾选核心中医症候信息，无法辨证推荐方药。"

    tcm_integration = ""
    if cb_never: 
        if sua >= 600:
            tcm_integration = f"当前血尿酸 ≥ 600μmol/L，**推荐起始中西医结合治疗**。"
        else:
            tcm_integration = f"血尿酸 &lt; 600μmol/L，**首选单纯中医药治疗**；若调理3个月未达标则改为中西结合。"
    elif cb_acute: 
        if (cb_cold + cb_damp + cb_def) >= 1: 
            tcm_integration = "急性期症状明显，**推荐中西医结合治疗**（中药内服外敷 + 西药抗炎镇痛）。"
        else:
            tcm_integration = "急性期症状轻微时可试用单纯中医药。"
    elif cb_tophi: 
        if sua >= 540 or (cb_cold + cb_damp + cb_def) >= 1:
            tcm_integration = f"慢性期且血尿酸 ≥ 540μmol/L，**推荐开启中西医结合治疗**。"
        else:
            tcm_integration = "血尿酸 &lt; 540μmol/L 且证候稳定时，可尝试单纯中医药治疗。"
    else: 
        if sua >= 600:
            tcm_integration = f"间歇期血尿酸 ≥ 600μmol/L，**推荐中西医结合治疗**。"
        else:
            tcm_integration = "血尿酸达到启动标准但 &lt; 600μmol/L 时，可首选单纯中医药治疗。"

    # ================= 渲染结果卡片 =================
    st.success(f"**系统推断分期：** {clinical_state}")
    
    st.markdown("### 📘 一、基于《中国指南》(2024版) 推荐")
    st.info(f"**🎯 治疗靶标：** {cn_target}  \n**⏱️ 降尿酸时机：** {cn_ult_init}  \n**💊 用药策略：** \n{cn_meds}")

    st.markdown("### 📙 二、基于《美国 ACR 指南》(2020版) 推荐")
    st.warning(f"**🎯 治疗靶标：** {acr_target}  \n**⏱️ 降尿酸时机：** {acr_ult_init}  \n**💊 用药策略：** \n{acr_meds}")

    st.markdown("### 🌿 三、基于《中西医结合诊疗指南》(2023版) 推荐")
    st.success(f"**☯️ 中医辨证：** {tcm_syndrome}  \n**🍵 经典方药：** {tcm_rx}  \n**⚡ 中西结合时机：** {tcm_integration}")
    
    st.caption("免责声明：本系统基于最新指南文献构建，仅供医疗决策辅助参考，不可替代专业医师的当面诊断。")
