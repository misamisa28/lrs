import os



import pandas as pd



# ---------- 配置 ----------



# (Excel 文件, 输出文件名前缀, 表单名列表)



DATA_DIR = 'data'



DATASETS = [

    ('京城大师赛.xlsx', '京城大师赛', ['S20','S21', 'S22']),

    ('粤小.xlsx', '粤小', ['S1', 'S2']),



]



DAYS = ['1', '2', '3', '4', '5']



STATE_COLS = [f'D{i}状态' for i in range(1, 6)]



D_COLUMN_VALUE_EXCLUDE_SUBSTR = ('状态', '发言顺序', '验人结果')



D_COLUMN_SPECIAL_VALUES = frozenset({'救', '自爆', '交牌', '拍刀', '弃票', 'out'})



DAOBAO_ROLES = ['盗宝通灵师', '盗宝毒师', '盗宝摄梦人', '盗宝蒙面人', '盗宝猎人']



JIXIE_SUB_ROLES = ['机械女巫', '机械猎人', '机械守卫', '机械通灵师', '机械双刀', '机械平民']



JIXIE_WOLF_ROLES = ['机械狼'] + JIXIE_SUB_ROLES



JIXIE_ROLES = JIXIE_SUB_ROLES



FIRST_CHECK_ROLES = ['预言家', '通灵师', '盗宝通灵师']



PROPHET_FIRST_CHECK_ROLES = ['预言家', '通灵师']



D1_SHERIFF_VOTE_COL = 'D1警下投票'



D1_SPEECH_ORDER_COL = 'D1发言顺序'



D1_SECOND_SHERIFF_VOTE_COL = 'D1二轮票'



NIGHT_TARGET1_COL = 'D1夜目标1'



SPECIAL_ORDER_EXILE_COL = '特殊放逐票'



SPECIAL_ORDER_EXILE_COL_LEGACY = '特殊放逐票（定序）'



D1_CHECK_RESULT_COL = 'D1验人结果'



D1_CHECK_RESULT_COL_LEGACY = 'D1结果'



D1_STATE_COL = 'D1状态'



D1_SHERIFF_BADGE_COL = 'D1警徽'



D1_EXILE_VOTE1_COL = 'D1放逐票1'



YVLHB_BANXING = '预女猎白混'



YVLHB_CHILDREN = ['预女猎白好人混', '预女猎白狼人混']



YVLHB_IDENTITY_COUNTS = {

    '狼': 4,

    '平民': 3,

    '预言家': 1,

    '女巫': 1,

    '猎人': 1,

    '白神': 1,



}



YVLHB_MIX_IDENTITIES = frozenset({'狼人混', '好人混'})



YVLHB_MIX_REQUIRED_COUNT = 1



YVLHB_ALLOWED_IDENTITIES = frozenset(YVLHB_IDENTITY_COUNTS) | YVLHB_MIX_IDENTITIES



JIXIE_BANXING = '机械狼'



JIXIE_IDENTITY_COUNTS = {

    '狼': 3,

    '平民': 4,

    '通灵师': 1,

    '女巫': 1,

    '猎人': 1,

    '守卫': 1,



}



JIXIE_MECH_REQUIRED_COUNT = 1



DAOBAO_IDENTITY_COUNTS = {

    '狼': 2,

    '狼王': 1,

    '平民': 4,



}



DAOBAO_POOL_ROLES = ('通灵师', '毒师', '猎人', '蒙面人', '摄梦人')



DAOBAO_POOL_REQUIRED_COUNT = 4



DAOBAO_MECH_REQUIRED_COUNT = 1



WOLF_ONLY_CAMP = {'狼人'}



NON_FIRST_WOLF_DATASET_PREFIX = '京城大师赛'



PLAIN_WOLF_IDENTITY = '狼'



RATE_COLS = {

    '狼人率': ('狼次数', '出场次数'),

    '预通率': ('预通次数', '出场次数'),

    '身份率': ('身份次数', '出场次数'),

    '总胜率': ('胜场次数', '出场次数'),

    '好人警下率': ('好人警下次数', '好人次数'),

    '好人胜率': ('好人胜利次数', '好人次数'),

    '放逐票正确率': ('正确放逐票次数', '放逐票次数'),

    '无预通放逐票正确率': ('无预通生推正确放逐票次数', '无预通放逐票次数'),

    '警徽票正确率': ('警徽票正确次数', '警徽票次数'),

    '平民放逐票正确率': ('平民正确放逐票次数', '平民放逐票次数'),

    '平民警徽票正确率': ('平民警徽票正确次数', '平民警徽票次数'),

    '毒药技能正确率': ('毒狼次数', '毒药使用次数'),

    '猎人技能正确率': ('猎人技能狼人次数', '猎人技能次数'),

    '狼人胜率': ('狼胜利次数', '狼次数'),

    '悍跳率': ('悍跳次数', '狼次数'),

    '首摄狼人率': ('首摄狼人次数', '摄梦人次数'),

    '盲毒狼人率': ('盲毒狼人次数', '盲毒次数'),



}



NON_FIRST_WOLF_RATE_COLS = {

    '非首局狼人率': ('非首局狼次数', '非首局出场次数'),



}



def get_rate_cols(include_non_first_wolf_rate=False):

    cols = dict(RATE_COLS)

    if include_non_first_wolf_rate:

        cols.update(NON_FIRST_WOLF_RATE_COLS)

    return cols



POISON_ROLES = ['女巫', '毒师']



BLIND_POISON_SAVE_MARK = '救'



BLIND_POISON_WOLF_CAMPS = {'狼人'}



HUNTER_ROLE = '猎人'



HUNTER_SKILL_INVALID_MARKS = frozenset({'√', '×', '✓', '✗', 'x', 'X'})



HUNTER_SKILL_WOLF_CAMPS = {'狼人'}



GOOD_IDENTITIES = {

    '平民', '预言家', '女巫', '通灵师', '猎人', '守卫', '摄梦人', '毒师', '好人混',



}



DREAM_FIRST_SPECIAL_IDENTITIES = {'狼王', '盗宝猎人'}



RED_WOLF_IDENTITIES = ['狼', '狼王', '黑狼王', '狼术师', '狼美人', '诡术师']



D1_WOLF_KNIFE_COL = 'D1狼刀'



DAOBAO_MASTER_BANXING = '盗宝大师'



DAOBAO_MEDIUM_ROLE = '盗宝通灵师'



ARCANE_BANXING = '诡术之境'



ARCANE_MASTER_ROLE = '诡术师'



CIVILIAN_IDENTITIES = {'平民', '好人混'}



WOLF_MIX_IDENTITIES = {'狼人混'}



MIXED_BLOOD_ROLES = {'好人混', '狼人混'}



WOLF_IDENTITIES_ORDERED = [

    '假面', '典狱长', '捣蛋鬼', '梦魇', '狼', '狼术师', '狼王', '狼美人', '石像鬼', '诡术师', '黑狼王',



]



WOLF_IDENTITIES = set(WOLF_IDENTITIES_ORDERED)



RULES_FILE = '规则.json'



def build_statistics_rules():

    """汇总统计规则（与 notebook 常量及标记逻辑一致），输出完整文档结构。"""

    dataset_desc = '、'.join(

        f"{prefix} {'/'.join(sheets)}" for _, prefix, sheets in DATASETS

    )

    wolf_id_text = '、'.join(WOLF_IDENTITIES_ORDERED)

    red_wolf_text = '、'.join(RED_WOLF_IDENTITIES)

    poison_roles_text = '/'.join(POISON_ROLES)

    good_id_text = '/'.join(sorted(GOOD_IDENTITIES))

    first_check_text = '、'.join(FIRST_CHECK_ROLES)

    rate_rules = {k: f"{v[0]} ÷ {v[1]}" for k, v in get_rate_cols(True).items()}

    rate_rules['说明'] = '分母为 0 记 0；百分比保留一位小数'

    rate_rules['非首局狼人率说明'] = (

        '仅京城大师赛产出；粤小不统计。'

        '非首局 = 日期末两位非 01；分子仅计身份为狼'

    )

    return {

        '说明': (

            '与 statistics.ipynb 代码一致。'

            '一局 = 日期 + 版型；好人侧 = 阵营非狼人/狼人混。'

        ),

        '数据来源与处理流程': {

            '输入': f'Excel（{dataset_desc}）',

            '步骤': [

                '身份推导阵营',

                '导出原始数据 JSON（删技能使用情况/其他，阵营紧跟身份）',

                '补充放逐票目标阵营',

                '生成标记，汇总玩家/版型/同边统计',

                '输出 JSON、Excel 至 data',

                '导出本规则至 规则.json',

            ],

        },

        '阵营推导': {

            '规则': '由身份列推导阵营',

            '映射': [

                f"{'、'.join(sorted(CIVILIAN_IDENTITIES))} → 平民",

                '狼人混 → 狼人混',

                f'{wolf_id_text}，或含盗宝/机械/傀儡 → 狼人',

                '其余 → 神职',

            ],

            '好人侧': '非狼人、非狼人混',

            '狼人侧': '狼人、狼人混',

        },

        '存活天数': {

            '个人': 'D1–D5 状态首个有记录的天数；全无则取对局持续天数',

            '对局持续': '同局任一人有状态记录的天数，取最大',

            '平均': '存活天数总和 ÷ 出场次数',

            '狼人均': '狼侧存活天数 ÷ 狼次数',

            '好人均': '好人侧存活天数 ÷ 好人次数',

        },

        '基础对局标记': {

            '胜利标记': '胜利方为狼或好人',

            '狼标记': '狼人侧',

            '好人标记': '非狼人侧',

            '身份标记': '神职、狼人、狼人混',

            '预通标记': '预言家或通灵师',

            '神职身份标记': '神职阵营',

            '机械狼标记': f'机械狼或{"、".join(JIXIE_SUB_ROLES)}',

            '机械子身份标记': '对应机械子身份记 1',

            '好人胜利标记': '平民/神职且好人赢',

            '狼胜利标记': '狼人侧且狼赢',

        },

        '女巫与毒药': {

            '女巫毒师标记': f'身份为{poison_roles_text}',

            '压毒标记': f'{poison_roles_text}，所有夜目标1 为空或救',

            '毒药使用标记': f'{poison_roles_text}，任一夜目标1 非空且非救',

            '毒狼人标记': '有毒药使用，且目标阵营为狼人',

            '盲毒标记': f'{poison_roles_text}，D1夜目标1 非空且非救',

            '盲毒狼人标记': '有盲毒，且 D1 目标阵营为狼人',

            '被盲毒标记': 'D1状态 = 被毒',

            '非狼被盲毒标记': '被盲毒且阵营非狼人',

        },

        '猎人与守卫与摄梦人': {

            '猎人标记': '身份为猎人',

            '猎人次数': '猎人局数合计',

            '守卫标记': '身份为守卫',

            '摄梦人标记': '身份为摄梦人',

            '首摄狼人标记': f'摄梦人 D1夜目标1 非空，目标身份非好人（{good_id_text}）',

            '首摄狼王盗宝猎人标记': f'摄梦人 D1夜目标1 非空，目标为{"、".join(sorted(DREAM_FIRST_SPECIAL_IDENTITIES))}',

            '猎人技能次数': f'猎人，技能列有有效目标（非 √/×）',

            '猎人技能狼人次数': '上述目标在同局阵营为狼人',

            '猎人技能正确率': '猎人技能狼人次数 ÷ 猎人技能次数',

        },

        '预言家与警徽票': {

            '起跳预言家标记': [

                '真预/通灵：身份为预言家或通灵师，D1验人 有值',

                '悍跳：好人侧非预/通灵，D1验人 有值，且本局真预/通灵均未验人',

            ],

            '警下标记': '好人侧且 D1发言顺序 = 警下',

            '第一轮警徽票正确': '警下、D1警下投票 有值，投给本局起跳预言家',

            '第二轮警徽票正确': '好人侧、D1二轮票 有值，投给起跳预言家',

            '警徽票正确标记': '一、二轮正确之和',

            '警徽票次数': '好人侧 D1警下投票 + D1二轮票（有列则计）',

            '平民警徽票次数': '警徽票次数且身份为平民',

            '平民警徽票正确次数': '警徽票正确且身份为平民',

            '警上站狼边': '有警徽票无正确票时，记「真预/通灵-悍跳狼」，逗号连接',

            '盗宝大师通灵师局排除': (

                f'{DAOBAO_MASTER_BANXING} 且有 {DAOBAO_MEDIUM_ROLE} 时，'

                '不计警徽票次数/正确次数及平民警徽票衍生项'

            ),

            '预通被放逐标记': '身份为预言家或通灵师，任一含「状态」列 = 被放逐',

            '预通被毒标记': '身份为预言家或通灵师，任一含「状态」列 = 被毒',

            '预通被枪标记': '身份为预言家或通灵师，任一含「状态」列 = 被枪',

            '预通获警徽标记': f'身份为预言家或通灵师，{D1_SHERIFF_BADGE_COL} = 该玩家姓名',

            '预通被奶死标记': '身份为预言家或通灵师，任一含「状态」列 = 同守同救out',

            '预通被盲毒标记': f'身份为预言家或通灵师，{D1_STATE_COL} = 被毒',

            '预通被代跳标记': '身份为预言家或通灵师，D1验人 为空，且同局有好人侧 D1验人 有值',

        },

        '悍跳与自爆': {

            '悍跳标记': '狼人侧且 D1验人 非空',

            '自爆标记': '狼人侧且 D1–D5 状态 任一天 = 自爆',

        },

        '放逐票': {

            '可投票': '非预言家、非通灵师',

            '单次放逐票': '好人侧、D{n}放逐票 有值、可投票',

            '正确放逐票': '有放逐票且目标阵营为狼人',

            '诡术之境特殊': {

                '版型': ARCANE_BANXING,

                '触发': f'{ARCANE_MASTER_ROLE} 同日夜目标1、2 均有值 A/B，且 A/B 一狼一好人',

                '正确': '好人可投票者投 A/B 中的好人，亦算正确（与投狼叠加）',

            },

            '特殊放逐票': f'{SPECIAL_ORDER_EXILE_COL} 有值且可投票',

            '特殊正确放逐票': '特殊放逐票有效且目标为狼人',

            '正确放逐票总计': 'D1–D5 放逐票1/2 正确 + 特殊正确',

            '放逐票次数总计': 'D1–D5 放逐票1/2 + 特殊放逐票',

            '无预通生推可统计日': {

                '预通存活': '本局预/通灵该天状态为空',

                '预通被放逐首日': '预/通灵该天状态首次为被放逐',

                '可统计': '以上均不满足；无预/通灵则每天可统计',

            },

            '无预通生推正确放逐票': '正确放逐票中，仅计可统计日',

            '无预通放逐票': '放逐票次数中，仅计可统计日',

            '平民放逐票次数': '放逐票总计且身份为平民',

            '平民正确放逐票次数': '正确放逐票总计且身份为平民',

        },

        '放逐票目标阵营': {

            '范围': 'D1–D5 放逐票1/2、特殊放逐票',

            '方法': '按日期+目标姓名匹配阵营',

            '特殊': '目标为预通记空；无法匹配记错误',

        },

        '首验与混血儿': {

            '被首验标记': f'同局 {first_check_text} 的 D1夜目标1 指向该玩家',

            '混血儿榜样标记': '同局好人混/狼人混的 D1夜目标1 指向该玩家',

        },

        '假金': {

            '发假金': '狼人侧验人非空、非查杀，被验者非狼侧',

            '接狼人金水': '非狼侧被悍跳狼发金水',

            '接狼人金水文本': '按被发金者汇总悍跳狼姓名（次数）',

        },

        '拉杆': {

            '拉杆标记': '通灵师板、有悍跳、验人结果非金水/查杀',

            '拉杆成功': '有拉杆且验人目标身份 = 验人结果',

            '拉杆记录': '成功明细：日期-姓名-验人-结果，逗号连接',

        },

        '非首局狼人率': {

            '范围': f'仅 {NON_FIRST_WOLF_DATASET_PREFIX} 各赛季玩家统计',

            '非首局': '日期编码末两位不为 01（01 为当天首局，整局排除）',

            '分子': f'非首局中身份为「{PLAIN_WOLF_IDENTITY}」的出场次数',

            '分母': '非首局出场次数',

            '比率': '非首局狼次数 ÷ 非首局出场次数',

            '粤小': '不产出非首局狼次数、非首局出场次数、非首局狼人率',

        },

        '红狼与狼刀': {

            '技能狼标记': '狼人阵营且身份非狼',

            '非盗宝红狼标记': f'身份为{red_wolf_text}，版型非{DAOBAO_MASTER_BANXING}',

            '自刀标记': '非盗宝红狼，D1狼刀 指向自己',

            '狼队友自刀标记': '非盗宝红狼，D1狼刀 指向另一名非盗宝红狼',

            '首刀女巫标记': '狼人阵营，D1狼刀 指向女巫',

        },

        '文本汇总': {

            '参与场次': '日期（版型，身份），按日期降序',

            '胜利场次': '参与场次中胜场',

            '首验': '预/通灵 D1夜目标1 → 姓名（次数）',

            '被首验': '被首验者汇总首验人（次数）',

            '盲毒狼人': '盲毒到的狼人姓名（次数）',

            '毒药记录': '毒药目标身份（次数），按次数降序',

            '猎人技能记录': '猎人技能目标身份（次数），按次数降序',

            '混血儿记录': '榜样姓名（狼/好人，次数），按次数降序',

            '接狼人金水': '发金悍跳狼姓名（次数）',

            '拉杆记录': '日期-姓名-验人-结果',

            '警上站狼边': '真预/通灵-悍跳狼',

            '预通滴滴记录': '预通被代跳局中，同局 D1验人 有值的好人姓名，顿号连接',

            '身份胜率': '各身份出场次数与胜率，格式：身份（次数，胜率），按次数降序',

            '版型胜率': '各版型出场次数与胜率，格式：版型（次数，胜率），按次数降序',

            '版型狼人率': '各版型出场次数与狼人率（阵营为狼人的概率），格式：版型（次数，狼人率），按次数降序',

            '座位号次数': '每局按行顺序依次为1号位起，汇总各座位号总次数，格式「座位号（次数）」'

        },

        '玩家统计比率': rate_rules,

        '版型统计': {

            '拆分': {

                '预女猎白混': '有狼人混→预女猎白狼人混；有好人混→预女猎白好人混',

                '盗宝大师': f'按子身份（{"、".join(DAOBAO_ROLES)}）分别计',

                '机械狼': '机械狼总版型 + 各机械子身份',

                '其他': '原版型名',

            },

            '指标': {

                '总场次': '出现次数',

                '狼赢/好人赢': '按胜利方统计',

                '平均持续天数': '对局持续天数均值',

                '狼人胜率': '狼赢 ÷ 总场次',

            },

            '汇总': [

                '预女猎白混 = 好人混版 + 狼人混版加权',

                '盗宝大师 = 各盗宝子身份加权',

            ],

            '缺失补零': '未出现的盗宝/机械/预女猎白子版型补 0',

        },

        '多赛季合并': {

            '场次/狼赢': '同版型直接相加',

            '平均持续天数': '按场次加权',

            '狼人胜率': '合并狼赢 ÷ 合并总场次',

        },

        '同边统计': {

            '范围': '出场 ≥ 6，同局两两配对',

            '同场次数': '同局次数',

            '同边': '同狼侧或同好人侧',

            '同边率': '同边 ÷ 同场',

            '同边狼人胜率': '同边狼且狼赢 ÷ 同边狼人次数',

            '同边好人胜率': '同边好人且好人赢 ÷ 同好人次数',

            '同边场次': '同边各局记录：日期（姓名A：身份、姓名B：身份、胜利方：结果），逗号连接',

        },

        '数据校验': {

            'D列取值': (

                '列名以 D1–D5 开头，且列名不含状态/发言顺序/验人结果；'

                '取值须为空、救/自爆/交牌/拍刀/弃票/out，或该日期对局中的玩家姓名'

            ),

            '预女猎白混身份': (

                '版型为预女猎白混时，身份须且仅有：4狼、3平民、1狼人混或好人混、'

                '预言家/女巫/猎人/白神各1；不可同时出现狼人混与好人混'

            ),

            '机械狼身份': (

                '版型为机械狼时，身份须且仅有：3狼、4平民、1个含「机械」的身份、'

                '通灵师/女巫/猎人/守卫各1'

            ),

            '盗宝大师身份': (

                '版型为盗宝大师时，身份须且仅有：2狼、1狼王、4平民、1个含「盗宝」的身份、'

                '通灵师/毒师/猎人/蒙面人/摄梦人五选四（各至多1）'

            ),

            'D1被放逐放逐票': (

                '若该局有人 D1状态 为被放逐，则 D1放逐票1 不得全员为空'

            ),

        },

        '原始数据导出': {

            '删除列': '技能使用情况、其他',

            '列名统一': '特殊放逐票（定序）→ 特殊放逐票；D1结果 → D1验人结果',

            '列顺序': '阵营紧跟身份',

            '行顺序': '保持 Excel 原序',

        },

        '角色常量': {

            '好人身份': sorted(GOOD_IDENTITIES),

            '盗宝子版型': DAOBAO_ROLES,

            '机械狼角色': JIXIE_WOLF_ROLES,

            '机械子版型': JIXIE_ROLES,

            '首验角色': FIRST_CHECK_ROLES,

            '预言家首验角色': PROPHET_FIRST_CHECK_ROLES,

        },

    }



def export_statistics_rules(path=RULES_FILE):

    import json

    rules = build_statistics_rules()

    with open(path, 'w', encoding='utf-8') as f:

        json.dump(rules, f, ensure_ascii=False, indent=4)

    return rules



# ---------- 工具函数 ----------



def camp_from_identity(identity):

    """根据身份推导阵营：假面/典狱长/捣蛋鬼/梦魇/狼/狼术师/狼王/狼美人/石像鬼/诡术师/黑狼王，或含盗宝/机械/傀儡 → 狼人。"""

    if pd.isna(identity):

        return '神职'

    identity = str(identity).strip()

    if not identity or identity == '<NA>':

        return '神职'

    if identity in CIVILIAN_IDENTITIES:

        return '平民'

    if identity in WOLF_MIX_IDENTITIES:

        return '狼人混'

    if (

        identity in WOLF_IDENTITIES

        or '盗宝' in identity

        or '机械' in identity

        or '傀儡' in identity

    ):

        return '狼人'

    return '神职'



def assign_camp_from_identity(data):

    """用身份列覆盖阵营列。"""

    data = data.copy()

    if '姓名' in data.columns:

        data['姓名'] = data['姓名'].astype('string').str.strip()

    data['阵营'] = data['身份'].map(camp_from_identity)

    return data



GOOD_WIN_CAMPS = {'平民', '神职'}



WOLF_WIN_CAMPS = {'狼人', '狼人混'}



def _is_first_session_game(date_val):

    """日期编码末两位为 01 表示当天首局。"""

    if pd.isna(date_val):

        return False

    text = str(date_val).strip()

    if not text or text in ('<NA>', 'None', 'nan'):

        return False

    if text.endswith('.0'):

        text = text[:-2]

    return text.endswith('01')



def _cell_has_value(value):

    if pd.isna(value):

        return False

    text = str(value).strip()

    return text != '' and text != '<NA>'



def _vote_has_value(series):

    vote = series.astype('string').str.strip()

    return series.notna() & (vote != '') & (vote != '<NA>')



def check_victory_camp_consistency(data, tag=''):

    """胜利方与身份推导阵营不一致时，提醒对应日期。"""

    required = {'日期', '姓名', '身份', '阵营', '胜利'}

    if not required.issubset(data.columns):

        return []

    win = data['胜利'].astype('string').str.strip()

    good_bad = data.loc[(win == '好人') & ~data['阵营'].isin(GOOD_WIN_CAMPS)]

    wolf_bad = data.loc[(win == '狼') & ~data['阵营'].isin(WOLF_WIN_CAMPS)]

    prefix = f'[{tag}] ' if tag else ''

    for side, bad_df in (('好人', good_bad), ('狼', wolf_bad)):

        if bad_df.empty:

            continue

        for date, group in bad_df.groupby('日期', sort=True):

            details = '、'.join(

                f"{row['姓名']}（身份={row['身份']}，阵营={row['阵营']}）"

                for _, row in group.iterrows()

            )

            print(f"{prefix}胜利为{side}但阵营不符：日期 {date} — {details}")

    if good_bad.empty and wolf_bad.empty:

        return []

    return pd.concat([good_bad, wolf_bad], ignore_index=True)



def check_sheriff_vote_consistency(data, tag=''):

    """警下须有投票，或本场全员无投票；非警下投票须为空。"""

    required = {'日期', '姓名', D1_SPEECH_ORDER_COL, D1_SHERIFF_VOTE_COL}

    if not required.issubset(data.columns):

        return []

    order = data[D1_SPEECH_ORDER_COL].astype('string').str.strip()

    vote_filled = _vote_has_value(data[D1_SHERIFF_VOTE_COL])

    is_under_sheriff = order == '警下'

    any_vote_in_game = vote_filled.groupby(data['日期']).transform('any')

    bad_under = is_under_sheriff & ~vote_filled & any_vote_in_game

    bad_other = ~is_under_sheriff & vote_filled

    bad = data.loc[bad_under | bad_other]

    if bad.empty:

        return []

    prefix = f'[{tag}] ' if tag else ''

    for date, group in bad.groupby('日期', sort=True):

        details = '、'.join(

            (

                f"{row['姓名']}（警下但{D1_SHERIFF_VOTE_COL}为空，且本场其他玩家有投票）"

                if str(row[D1_SPEECH_ORDER_COL]).strip() == '警下'

                else f"{row['姓名']}（非警下但{D1_SHERIFF_VOTE_COL}={row[D1_SHERIFF_VOTE_COL]}）"

            )

            for _, row in group.iterrows()

        )

        print(f"{prefix}{D1_SPEECH_ORDER_COL}与{D1_SHERIFF_VOTE_COL}不符：日期 {date} — {details}")

    return bad.reset_index(drop=True)



def check_civilian_night_columns(data, tag=''):

    """平民在含狼刀/夜目标1/夜目标2的列须均为空。"""

    required = {'日期', '姓名', '身份'}

    if not required.issubset(data.columns):

        return []

    night_cols = [

        col for col in data.columns

        if '狼刀' in col or '夜目标1' in col or '夜目标2' in col

    ]

    if not night_cols:

        return []

    civilians = data[data['身份'].astype('string').str.strip() == '平民']

    if civilians.empty:

        return []

    bad_rows = []

    for _, row in civilians.iterrows():

        bad_cols = [col for col in night_cols if _cell_has_value(row[col])]

        if bad_cols:

            bad_rows.append((row, bad_cols))

    if not bad_rows:

        return []

    prefix = f'[{tag}] ' if tag else ''

    by_date = {}

    for row, bad_cols in bad_rows:

        date = row['日期']

        detail = f"{row['姓名']}（{', '.join(f'{col}={row[col]}' for col in bad_cols)}）"

        by_date.setdefault(date, []).append(detail)

    for date in sorted(by_date, key=lambda x: (str(type(x)), str(x))):

        details = '、'.join(by_date[date])

        print(f"{prefix}平民狼刀/夜目标列须为空：日期 {date} — {details}")

    return pd.DataFrame(

        [{'日期': row['日期'], '姓名': row['姓名'], '身份': row['身份'], '异常列': '、'.join(bad_cols)}

         for row, bad_cols in bad_rows]

    )



def _adjacent_wolf_knife_col(cols, state_col):

    """状态列之后最近的一列狼刀列。"""

    for col in cols[cols.index(state_col) + 1:]:

        if '狼刀' in col:

            return col

    return None



def check_state_after_columns_empty(data, tag=''):

    """状态列有值后，该列之后除特殊放逐票、阵营、其他状态列外须均为空；首次自爆时相邻狼刀可非空。"""

    required = {'日期', '姓名'}

    if not required.issubset(data.columns):

        return []

    cols = list(data.columns)

    state_cols = [col for col in cols if '状态' in col]

    if not state_cols:

        return []

    bad_rows = []

    for _, row in data.iterrows():

        first_state_col = next(

            (col for col in state_cols if _cell_has_value(row[col])),

            None,

        )

        for state_col in state_cols:

            if not _cell_has_value(row[state_col]):

                continue

            allowed_extra = set()

            if (

                state_col == first_state_col

                and str(row[state_col]).strip() == '自爆'

            ):

                adj_knife = _adjacent_wolf_knife_col(cols, state_col)

                if adj_knife:

                    allowed_extra.add(adj_knife)

            after_cols = [

                col for col in cols[cols.index(state_col) + 1:]

                if col not in {SPECIAL_ORDER_EXILE_COL, '阵营'}

                and '状态' not in col

                and col not in allowed_extra

            ]

            bad_cols = [col for col in after_cols if _cell_has_value(row[col])]

            if bad_cols:

                bad_rows.append((row, state_col, bad_cols))

    if not bad_rows:

        return []

    prefix = f'[{tag}] ' if tag else ''

    by_date = {}

    for row, state_col, bad_cols in bad_rows:

        date = row['日期']

        detail = (

            f"{row['姓名']}（{state_col}={row[state_col]}，"

            f"后续非空列：{', '.join(f'{col}={row[col]}' for col in bad_cols)}）"

        )

        by_date.setdefault(date, []).append(detail)

    for date in sorted(by_date, key=lambda x: (str(type(x)), str(x))):

        details = '、'.join(by_date[date])

        print(f"{prefix}状态列之后须为空：日期 {date} — {details}")

    return pd.DataFrame(

        [

            {

                '日期': row['日期'],

                '姓名': row['姓名'],

                '状态列': state_col,

                '异常列': '、'.join(bad_cols),

            }

            for row, state_col, bad_cols in bad_rows

        ]

    )



def check_wolf_knife_camp(data, tag=''):

    """仅阵营为狼人的玩家可在狼刀列有值。"""

    required = {'日期', '姓名', '身份', '阵营'}

    if not required.issubset(data.columns):

        return []

    knife_cols = [col for col in data.columns if '狼刀' in col]

    if not knife_cols:

        return []

    bad_rows = []

    for _, row in data.iterrows():

        if str(row['阵营']).strip() == '狼人':

            continue

        bad_cols = [col for col in knife_cols if _cell_has_value(row[col])]

        if bad_cols:

            bad_rows.append((row, bad_cols))

    if not bad_rows:

        return []

    prefix = f'[{tag}] ' if tag else ''

    by_date = {}

    for row, bad_cols in bad_rows:

        date = row['日期']

        detail = (

            f"{row['姓名']}（身份={row['身份']}，阵营={row['阵营']}，"

            f"{', '.join(f'{col}={row[col]}' for col in bad_cols)}）"

        )

        by_date.setdefault(date, []).append(detail)

    for date in sorted(by_date, key=lambda x: (str(type(x)), str(x))):

        details = '、'.join(by_date[date])

        print(f"{prefix}仅狼人可有狼刀：日期 {date} — {details}")

    return pd.DataFrame(

        [

            {

                '日期': row['日期'],

                '姓名': row['姓名'],

                '身份': row['身份'],

                '阵营': row['阵营'],

                '异常列': '、'.join(bad_cols),

            }

            for row, bad_cols in bad_rows

        ]

    )



def check_wolf_camp_count_per_game(data, tag=''):

    """所有版型都须4个狼人阵营（不含狼人混）。"""

    required = {'日期', '版型', '姓名', '身份', '阵营'}

    if not required.issubset(data.columns):

        return []

    bad_games = []

    for (date, banxing), group in data.groupby(['日期', '版型'], sort=True):

        wolf_players = group[group['阵营'].isin(WOLF_ONLY_CAMP)]

        wolf_count = len(wolf_players)

        expected = 4

        if wolf_count != expected:

            bad_games.append((date, banxing, wolf_count, expected, wolf_players))

    if not bad_games:

        return []

    prefix = f'[{tag}] ' if tag else ''

    for date, banxing, wolf_count, expected, wolf_players in bad_games:

        if wolf_players.empty:

            wolf_detail = '无'

        else:

            wolf_detail = '、'.join(

                f"{row['姓名']}（{row['身份']}）"

                for _, row in wolf_players.iterrows()

            )

        print(

            f"{prefix}狼人阵营人数不符：日期 {date}（版型={banxing}）"

            f" — 应有 {expected} 人，实际 {wolf_count} 人：{wolf_detail}"

        )

    return pd.DataFrame(

        [

            {

                '日期': date,

                '版型': banxing,

                '应有狼人数': expected,

                '实际狼人数': wolf_count,

            }

            for date, banxing, wolf_count, expected, _ in bad_games

        ]

    )



def check_self_explode_wolf_only(data, tag=''):

    """仅阵营为狼人的玩家可在状态列出现自爆。"""

    required = {'日期', '姓名', '身份', '阵营'}

    if not required.issubset(data.columns):

        return []

    state_cols = [col for col in data.columns if '状态' in col]

    if not state_cols:

        return []

    bad_rows = []

    for _, row in data.iterrows():

        if str(row['阵营']).strip() == '狼人':

            continue

        bad_cols = [

            col for col in state_cols

            if _cell_has_value(row[col]) and str(row[col]).strip() == '自爆'

        ]

        if bad_cols:

            bad_rows.append((row, bad_cols))

    if not bad_rows:

        return []

    prefix = f'[{tag}] ' if tag else ''

    by_date = {}

    for row, bad_cols in bad_rows:

        date = row['日期']

        detail = (

            f"{row['姓名']}（身份={row['身份']}，阵营={row['阵营']}，"

            f"{', '.join(bad_cols)}）"

        )

        by_date.setdefault(date, []).append(detail)

    for date in sorted(by_date, key=lambda x: (str(type(x)), str(x))):

        details = '、'.join(by_date[date])

        print(f"{prefix}仅狼人可自爆：日期 {date} — {details}")

    return pd.DataFrame(

        [

            {

                '日期': row['日期'],

                '姓名': row['姓名'],

                '身份': row['身份'],

                '阵营': row['阵营'],

                '异常列': '、'.join(bad_cols),

            }

            for row, bad_cols in bad_rows

        ]

    )



def check_mixed_blood_night_target1(data, tag=''):

    """好人混/狼人混的 D1夜目标1 不得为空。"""

    required = {'日期', '姓名', '身份', NIGHT_TARGET1_COL}

    if not required.issubset(data.columns):

        return []

    mixed = data[data['身份'].isin(MIXED_BLOOD_ROLES)]

    if mixed.empty:

        return []

    target = mixed[NIGHT_TARGET1_COL].astype('string').str.strip()

    bad = mixed.loc[

        mixed[NIGHT_TARGET1_COL].isna()

        | (target == '')

        | (target == '<NA>')

    ]

    if bad.empty:

        return []

    prefix = f'[{tag}] ' if tag else ''

    for date, group in bad.groupby('日期', sort=True):

        details = '、'.join(

            f"{row['姓名']}（身份={row['身份']}）"

            for _, row in group.iterrows()

        )

        print(f"{prefix}混血儿{NIGHT_TARGET1_COL}不得为空：日期 {date} — {details}")

    return bad.reset_index(drop=True)



def check_mixed_blood_model_camp(data, tag=''):

    """好人混榜样阵营不得为狼人侧；狼人混榜样阵营不得为好人侧。"""

    required = {'日期', '版型', '姓名', '身份', NIGHT_TARGET1_COL}

    if not required.issubset(data.columns):

        return []

    game_keys = ['日期', '版型']

    mixed = data[data['身份'].isin(MIXED_BLOOD_ROLES)].copy()

    if mixed.empty:

        return []

    target = mixed[NIGHT_TARGET1_COL].astype('string').str.strip()

    mixed = mixed[

        mixed[NIGHT_TARGET1_COL].notna()

        & (target != '')

        & (target != '<NA>')

        & (target != '救')

    ].copy()

    if mixed.empty:

        return []

    mixed['_model_target'] = mixed[NIGHT_TARGET1_COL].astype('string').str.strip()

    lookup = (

        data[game_keys + ['姓名', '阵营']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': '_model_target', '阵营': '_target_camp'})

    )

    events = mixed.merge(lookup, on=game_keys + ['_model_target'], how='left')

    camp = events['_target_camp'].astype('string').str.strip()

    events = events[

        events['_target_camp'].notna()

        & (camp != '')

        & (camp != '<NA>')

    ].copy()

    if events.empty:

        return []

    identity = events['身份'].astype('string').str.strip()

    good_mix_bad = events.loc[(identity == '好人混') & camp.isin(WOLF_WIN_CAMPS)]

    wolf_mix_bad = events.loc[(identity == '狼人混') & camp.isin(GOOD_WIN_CAMPS)]

    bad = pd.concat([good_mix_bad, wolf_mix_bad], ignore_index=True)

    if bad.empty:

        return []

    prefix = f'[{tag}] ' if tag else ''

    for date, group in bad.groupby('日期', sort=True):

        details = '、'.join(

            (

                f"{row['姓名']}（身份={row['身份']}，榜样={row['_model_target']}，"

                f"目标阵营={str(row['_target_camp']).strip()}，"

                f"要求={'不得为狼人' if str(row['身份']).strip() == '好人混' else '不得为好人'}）"

            )

            for _, row in group.iterrows()

        )

        print(f"{prefix}混血儿榜样阵营不符：日期 {date} — {details}")

    return bad.reset_index(drop=True)



def _d_columns_for_value_check(columns):

    """D1–D5 列，排除列名含状态/发言顺序/验人结果。"""

    return [

        col for col in columns

        if len(str(col)) >= 2

        and str(col)[0] == 'D'

        and str(col)[1] in DAYS

        and not any(sub in str(col) for sub in D_COLUMN_VALUE_EXCLUDE_SUBSTR)

    ]



def check_d_column_values(data, tag=''):

    """D 列（除状态/发言顺序/验人结果外）取值须为空、救/自爆/交牌/拍刀/弃票/out 或该局玩家姓名。"""

    required = {'日期', '姓名'}

    if not required.issubset(data.columns):

        return []

    check_cols = _d_columns_for_value_check(data.columns)

    if not check_cols:

        return []

    bad_rows = []

    for date, group in data.groupby('日期', sort=False):

        game_names = {

            str(name).strip()

            for name in group['姓名'].astype('string')

            if pd.notna(name) and str(name).strip() not in ('', '<NA>')

        }

        for _, row in group.iterrows():

            bad_cols = []

            for col in check_cols:

                if not _cell_has_value(row[col]):

                    continue

                val = str(row[col]).strip()

                if val in D_COLUMN_SPECIAL_VALUES or val in game_names:

                    continue

                bad_cols.append((col, val))

            if bad_cols:

                bad_rows.append((row, bad_cols))

    if not bad_rows:

        return []

    prefix = f'[{tag}] ' if tag else ''

    by_date = {}

    for row, bad_cols in bad_rows:

        date = row['日期']

        detail = '、'.join(f'{col}={val}' for col, val in bad_cols)

        by_date.setdefault(date, []).append(f"{row['姓名']}（{detail}）")

    for date in sorted(by_date, key=lambda x: (str(type(x)), str(x))):

        details = '、'.join(by_date[date])

        print(f"{prefix}D列取值非法：日期 {date} — {details}")

    return pd.DataFrame(

        [

            {

                '日期': row['日期'],

                '姓名': row['姓名'],

                '非法列': '、'.join(col for col, _ in bad_cols),

                '非法值': '、'.join(val for _, val in bad_cols),

            }

            for row, bad_cols in bad_rows

        ]

    )



def check_d1_exile_vote_when_exiled(data, tag=''):

    """有人 D1状态 为被放逐时，该局 D1放逐票1 不得全员为空。"""

    required = {'日期', '姓名', D1_STATE_COL, D1_EXILE_VOTE1_COL}

    if not required.issubset(data.columns):

        return []

    bad_games = []

    for date, group in data.groupby('日期', sort=True):

        exiled = group[D1_STATE_COL].astype('string').str.strip() == '被放逐'

        if not exiled.any():

            continue

        if not _vote_has_value(group[D1_EXILE_VOTE1_COL]).any():

            exiled_players = [

                str(name).strip()

                for name in group.loc[exiled, '姓名']

                if pd.notna(name) and str(name).strip() not in ('', '<NA>')

            ]

            bad_games.append((date, exiled_players))

    if not bad_games:

        return []

    prefix = f'[{tag}] ' if tag else ''

    bad_frames = []

    for date, exiled_players in bad_games:

        players_text = '、'.join(exiled_players) if exiled_players else '（未知）'

        print(

            f"{prefix}{D1_STATE_COL} 含被放逐但 {D1_EXILE_VOTE1_COL} 全员为空："

            f"日期 {date}，被放逐玩家 {players_text}"

        )

        bad_frames.append(data[data['日期'] == date])

    return pd.concat(bad_frames, ignore_index=True).drop_duplicates()



def check_yvlhb_identity_composition(data, tag=''):

    """预女猎白混对局身份须为 4狼、3平民、1狼人混或好人混、预言家、女巫、猎人、白神各1。"""

    required = {'日期', '版型', '姓名', '身份'}

    if not required.issubset(data.columns):

        return []

    bad_games = []

    for (date, banxing), group in data.groupby(['日期', '版型'], sort=True):

        if str(banxing).strip() != YVLHB_BANXING:

            continue

        identities = group['身份'].astype('string').str.strip()

        counts = identities.value_counts().to_dict()

        mix_count = sum(counts.get(role, 0) for role in YVLHB_MIX_IDENTITIES)

        unexpected = sorted(

            role for role in counts

            if role not in YVLHB_ALLOWED_IDENTITIES

            and role not in ('', '<NA>') and pd.notna(role)

        )

        mismatches = []

        for role, expected in YVLHB_IDENTITY_COUNTS.items():

            actual = counts.get(role, 0)

            if actual != expected:

                mismatches.append(f'{role}{actual}≠{expected}')

        if mix_count != YVLHB_MIX_REQUIRED_COUNT:

            mismatches.append(f'混血{mix_count}≠{YVLHB_MIX_REQUIRED_COUNT}')

        if counts.get('狼人混', 0) and counts.get('好人混', 0):

            mismatches.append('狼人混与好人混不可同局')

        if unexpected:

            mismatches.append('非法身份=' + '、'.join(unexpected))

        if mismatches:

            detail = '、'.join(f'{k}{v}' for k, v in sorted(counts.items()))

            bad_games.append((date, banxing, mismatches, detail))

    if not bad_games:

        return []

    prefix = f'[{tag}] ' if tag else ''

    for date, banxing, mismatches, detail in bad_games:

        issues = '；'.join(mismatches)

        print(

            f"{prefix}预女猎白混身份不符：日期 {date} — {issues}（{detail}）"

        )

    return pd.DataFrame(

        [

            {

                '日期': date,

                '版型': banxing,

                '问题': '；'.join(mismatches),

                '身份分布': detail,

            }

            for date, banxing, mismatches, detail in bad_games

        ]

    )



def _is_jixie_mechanical_role(role):

    return '机械' in str(role).strip()



def check_jixie_wolf_identity_composition(data, tag=''):

    """机械狼对局身份须为 3狼、4平民、1含机械身份、通灵师、女巫、猎人、守卫各1。"""

    required = {'日期', '版型', '姓名', '身份'}

    if not required.issubset(data.columns):

        return []

    bad_games = []

    for (date, banxing), group in data.groupby(['日期', '版型'], sort=True):

        if str(banxing).strip() != JIXIE_BANXING:

            continue

        identities = group['身份'].astype('string').str.strip()

        counts = identities.value_counts().to_dict()

        mech_roles = [role for role in counts if _is_jixie_mechanical_role(role)]

        mech_count = sum(counts[role] for role in mech_roles)

        unexpected = sorted(

            role for role in counts

            if role not in JIXIE_IDENTITY_COUNTS

            and not _is_jixie_mechanical_role(role)

            and role not in ('', '<NA>') and pd.notna(role)

        )

        mismatches = []

        for role, expected in JIXIE_IDENTITY_COUNTS.items():

            actual = counts.get(role, 0)

            if actual != expected:

                mismatches.append(f'{role}{actual}≠{expected}')

        if mech_count != JIXIE_MECH_REQUIRED_COUNT:

            if mech_roles:

                mech_detail = '、'.join(f'{r}{counts[r]}' for r in sorted(mech_roles))

                mismatches.append(f'机械身份{mech_count}≠{JIXIE_MECH_REQUIRED_COUNT}（{mech_detail}）')

            else:

                mismatches.append(f'机械身份{mech_count}≠{JIXIE_MECH_REQUIRED_COUNT}')

        if unexpected:

            mismatches.append('非法身份=' + '、'.join(unexpected))

        if mismatches:

            detail = '、'.join(f'{k}{v}' for k, v in sorted(counts.items()))

            bad_games.append((date, banxing, mismatches, detail))

    if not bad_games:

        return []

    prefix = f'[{tag}] ' if tag else ''

    for date, banxing, mismatches, detail in bad_games:

        issues = '；'.join(mismatches)

        print(

            f"{prefix}机械狼身份不符：日期 {date} — {issues}（{detail}）"

        )

    return pd.DataFrame(

        [

            {

                '日期': date,

                '版型': banxing,

                '问题': '；'.join(mismatches),

                '身份分布': detail,

            }

            for date, banxing, mismatches, detail in bad_games

        ]

    )



def _is_daobao_role(role):

    return '盗宝' in str(role).strip()



def check_daobao_master_identity_composition(data, tag=''):

    """盗宝大师对局身份须为 2狼、1狼王、4平民、1含盗宝身份，通灵师/毒师/猎人/蒙面人/摄梦人五选四。"""

    required = {'日期', '版型', '姓名', '身份'}

    if not required.issubset(data.columns):

        return []

    bad_games = []

    for (date, banxing), group in data.groupby(['日期', '版型'], sort=True):

        if str(banxing).strip() != DAOBAO_MASTER_BANXING:

            continue

        identities = group['身份'].astype('string').str.strip()

        counts = identities.value_counts().to_dict()

        daobao_roles = [role for role in counts if _is_daobao_role(role)]

        daobao_count = sum(counts[role] for role in daobao_roles)

        pool_hits = {role: counts.get(role, 0) for role in DAOBAO_POOL_ROLES}

        pool_count = sum(pool_hits.values())

        pool_missing = [role for role in DAOBAO_POOL_ROLES if pool_hits[role] == 0]

        pool_extra = [

            role for role in DAOBAO_POOL_ROLES

            if pool_hits[role] > 1

        ]

        allowed = set(DAOBAO_IDENTITY_COUNTS) | set(DAOBAO_POOL_ROLES)

        unexpected = sorted(

            role for role in counts

            if role not in allowed

            and not _is_daobao_role(role)

            and role not in ('', '<NA>') and pd.notna(role)

        )

        mismatches = []

        for role, expected in DAOBAO_IDENTITY_COUNTS.items():

            actual = counts.get(role, 0)

            if actual != expected:

                mismatches.append(f'{role}{actual}≠{expected}')

        if daobao_count != DAOBAO_MECH_REQUIRED_COUNT:

            if daobao_roles:

                daobao_detail = '、'.join(f'{r}{counts[r]}' for r in sorted(daobao_roles))

                mismatches.append(

                    f'盗宝身份{daobao_count}≠{DAOBAO_MECH_REQUIRED_COUNT}（{daobao_detail}）'

                )

            else:

                mismatches.append(f'盗宝身份{daobao_count}≠{DAOBAO_MECH_REQUIRED_COUNT}')

        if pool_count != DAOBAO_POOL_REQUIRED_COUNT:

            mismatches.append(f'神职池{pool_count}≠{DAOBAO_POOL_REQUIRED_COUNT}')

        if pool_extra:

            mismatches.append('神职池重复=' + '、'.join(

                f'{role}{pool_hits[role]}' for role in pool_extra

            ))

        if len(pool_missing) != len(DAOBAO_POOL_ROLES) - DAOBAO_POOL_REQUIRED_COUNT:

            mismatches.append('神职池缺=' + '、'.join(pool_missing))

        if unexpected:

            mismatches.append('非法身份=' + '、'.join(unexpected))

        if mismatches:

            detail = '、'.join(f'{k}{v}' for k, v in sorted(counts.items()))

            bad_games.append((date, banxing, mismatches, detail))

    if not bad_games:

        return []

    prefix = f'[{tag}] ' if tag else ''

    for date, banxing, mismatches, detail in bad_games:

        issues = '；'.join(mismatches)

        print(

            f"{prefix}盗宝大师身份不符：日期 {date} — {issues}（{detail}）"

        )

    return pd.DataFrame(

        [

            {

                '日期': date,

                '版型': banxing,

                '问题': '；'.join(mismatches),

                '身份分布': detail,

            }

            for date, banxing, mismatches, detail in bad_games

        ]

    )



def run_data_checks(data, tag=''):

    """依次运行全部数据校验规则（互不覆盖，各自独立输出）。"""

    check_victory_camp_consistency(data, tag=tag)

    check_sheriff_vote_consistency(data, tag=tag)

    check_civilian_night_columns(data, tag=tag)

    check_state_after_columns_empty(data, tag=tag)

    check_wolf_knife_camp(data, tag=tag)

    check_wolf_camp_count_per_game(data, tag=tag)

    check_self_explode_wolf_only(data, tag=tag)

    check_mixed_blood_night_target1(data, tag=tag)

    check_mixed_blood_model_camp(data, tag=tag)

    check_d_column_values(data, tag=tag)

    check_d1_exile_vote_when_exiled(data, tag=tag)

    check_yvlhb_identity_composition(data, tag=tag)

    check_jixie_wolf_identity_composition(data, tag=tag)

    check_daobao_master_identity_composition(data, tag=tag)



def normalize_special_exile_column(data):

    """Excel 旧列名「特殊放逐票（定序）」统一为「特殊放逐票」。"""

    if SPECIAL_ORDER_EXILE_COL_LEGACY not in data.columns:

        return data

    data = data.copy()

    if SPECIAL_ORDER_EXILE_COL in data.columns:

        data = data.drop(columns=[SPECIAL_ORDER_EXILE_COL_LEGACY])

    else:

        data = data.rename(columns={SPECIAL_ORDER_EXILE_COL_LEGACY: SPECIAL_ORDER_EXILE_COL})

    return data



def normalize_d1_check_result_column(data):

    """Excel 旧列名「D1结果」统一为「D1验人结果」。"""

    if D1_CHECK_RESULT_COL_LEGACY not in data.columns:

        return data

    data = data.copy()

    if D1_CHECK_RESULT_COL in data.columns:

        data = data.drop(columns=[D1_CHECK_RESULT_COL_LEGACY])

    else:

        data = data.rename(columns={D1_CHECK_RESULT_COL_LEGACY: D1_CHECK_RESULT_COL})

    return data



def prepare_raw_export_df(df):

    """原始数据导出：去掉无关列，并将计算出的阵营列紧跟身份列。"""

    raw = df.drop(columns=['技能使用情况', '其他'], errors='ignore')

    cols = list(raw.columns)

    if '身份' in cols and '阵营' in cols:

        cols.remove('阵营')

        cols.insert(cols.index('身份') + 1, '阵营')

        raw = raw[cols]

    return raw



def merge_vote_camps(data):

    """为放逐票补充目标阵营（预通不计入）。"""

    lookup_base = data[['日期', '姓名', '阵营']].drop_duplicates(subset=['日期', '姓名'])

    lookup_base['姓名'] = lookup_base['姓名'].astype('string')

    for day in DAYS:

        for n in ('1', '2'):

            vote_col = f'D{day}放逐票{n}'

            camp_col = f'{vote_col}阵营'

            if vote_col not in data.columns:

                continue

            lookup = lookup_base.rename(columns={'姓名': vote_col, '阵营': camp_col})

            data[vote_col] = data[vote_col].astype('string')

            data = data.merge(lookup, on=['日期', vote_col], how='left')

            is_yutong = data[vote_col] == '预通'

            data.loc[is_yutong, camp_col] = pd.NA

            data[camp_col] = data[camp_col].fillna('错误')

    if SPECIAL_ORDER_EXILE_COL in data.columns:

        camp_col = f'{SPECIAL_ORDER_EXILE_COL}阵营'

        lookup = lookup_base.rename(columns={'姓名': SPECIAL_ORDER_EXILE_COL, '阵营': camp_col})

        data[SPECIAL_ORDER_EXILE_COL] = data[SPECIAL_ORDER_EXILE_COL].astype('string')

        data = data.merge(lookup, on=['日期', SPECIAL_ORDER_EXILE_COL], how='left')

        is_yutong = data[SPECIAL_ORDER_EXILE_COL] == '预通'

        data.loc[is_yutong, camp_col] = pd.NA

        data[camp_col] = data[camp_col].fillna('错误')

    return data



def _has_state_value(val):

    if pd.isna(val):

        return False

    text = str(val).strip()

    return text not in ('', '<NA>')



def player_survival_days(row):

    """个人存活天数：D1→D5 首个非空状态天数；全无则 0（由 assign_survival_days 补为对局持续天数）。"""

    for i, col in enumerate(STATE_COLS, start=1):

        if _has_state_value(row.get(col)):

            return i

    return 0



def assign_survival_days(data):

    """个人存活天数；个人全无状态时等于对局持续天数。"""

    game_dur = (

        data.groupby(['日期', '版型'])

        .apply(game_duration, include_groups=False)

        .reset_index(name='对局持续天数')

    )

    data = data.merge(game_dur, on=['日期', '版型'], how='left')

    data['存活天数'] = data.apply(player_survival_days, axis=1)

    no_record = data['存活天数'] == 0

    data.loc[no_record, '存活天数'] = data.loc[no_record, '对局持续天数'].fillna(0)

    return data.drop(columns=['对局持续天数'])



def game_duration(group):

    """一局对局的持续天数（按该局状态列）。"""

    days = 0

    for i, col in enumerate(STATE_COLS, start=1):

        if group[col].notna().any():

            days = i

    return days



def split_banxing(banxing, group):

    """将一局拆分为统计用版型（预女猎白混 / 盗宝大师 / 机械狼需细分或汇总）。"""

    if banxing == '预女猎白混':

        ids = group['身份'].astype(str)

        if ids.str.contains('狼人混', na=False).any():

            return ['预女猎白狼人混']

        if ids.str.contains('好人混', na=False).any():

            return ['预女猎白好人混']

        return []

    if banxing == '盗宝大师':

        ids = group['身份'].astype(str)

        return [role for role in DAOBAO_ROLES if ids.eq(role).any()]

    if banxing == '机械狼':

        ids = group['身份'].astype(str)

        subs = [role for role in JIXIE_ROLES if ids.eq(role).any()]

        return ['机械狼'] + subs

    return [banxing]



def assign_first_check_markers(data):

    """同日期+版型中，预言家/通灵师/盗宝通灵师的 D1夜目标1 即为被首验玩家。"""

    game_keys = ['日期', '版型']

    if NIGHT_TARGET1_COL not in data.columns:

        data['被首验标记'] = 0

        return data

    targets = data.loc[

        data['身份'].isin(FIRST_CHECK_ROLES),

        [*game_keys, NIGHT_TARGET1_COL],

    ].dropna(subset=[NIGHT_TARGET1_COL])

    targets[NIGHT_TARGET1_COL] = targets[NIGHT_TARGET1_COL].astype(str).str.strip()

    targets = targets[targets[NIGHT_TARGET1_COL] != '']

    targets = (

        targets.rename(columns={NIGHT_TARGET1_COL: '姓名'})

        .drop_duplicates(subset=[*game_keys, '姓名'])

        .assign(被首验标记=1)

    )

    data = data.drop(columns=['被首验标记'], errors='ignore')

    data = data.merge(targets, on=[*game_keys, '姓名'], how='left')

    data['被首验标记'] = data['被首验标记'].fillna(0).astype(int)

    return data



def assign_mixed_blood_model_markers(data):

    """同日期+版型中，好人混/狼人混的 D1夜目标1 即为混血儿榜样玩家。"""

    game_keys = ['日期', '版型']

    if NIGHT_TARGET1_COL not in data.columns:

        data['混血儿榜样标记'] = 0

        return data

    targets = data.loc[

        data['身份'].isin(['好人混', '狼人混']),

        [*game_keys, NIGHT_TARGET1_COL],

    ].dropna(subset=[NIGHT_TARGET1_COL])

    targets[NIGHT_TARGET1_COL] = targets[NIGHT_TARGET1_COL].astype(str).str.strip()

    targets = targets[targets[NIGHT_TARGET1_COL] != '']

    targets = (

        targets.rename(columns={NIGHT_TARGET1_COL: '姓名'})

        .drop_duplicates(subset=[*game_keys, '姓名'])

        .assign(混血儿榜样标记=1)

    )

    data = data.drop(columns=['混血儿榜样标记'], errors='ignore')

    data = data.merge(targets, on=[*game_keys, '姓名'], how='left')

    data['混血儿榜样标记'] = data['混血儿榜样标记'].fillna(0).astype(int)

    return data



def summarize_mixed_blood_records(data):

    """混血儿记录：好人混/狼人混 D1夜目标1 对应玩家，按姓名与狼/好人汇总次数。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '混血儿记录': pd.Series(dtype=str)})

    game_keys = ['日期', '版型']

    if NIGHT_TARGET1_COL not in data.columns:

        return empty

    events = data.loc[

        data['身份'].isin(MIXED_BLOOD_ROLES),

        [*game_keys, '姓名', NIGHT_TARGET1_COL],

    ].copy()

    if events.empty:

        return empty

    target = events[NIGHT_TARGET1_COL].astype('string').str.strip()

    events = events[

        events[NIGHT_TARGET1_COL].notna()

        & (target != '')

        & (target != '<NA>')

        & (target != '救')

    ].copy()

    if events.empty:

        return empty

    events['_model_target'] = events[NIGHT_TARGET1_COL].astype('string').str.strip()

    lookup = (

        data[game_keys + ['姓名', '阵营']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': '_model_target', '阵营': '_target_camp'})

    )

    events = events.merge(lookup, on=game_keys + ['_model_target'], how='left')

    camp = events['_target_camp'].astype('string').str.strip()

    events = events[

        events['_target_camp'].notna()

        & (camp != '')

        & (camp != '<NA>')

    ].copy()

    if events.empty:

        return empty

    events['_side_label'] = camp.map(

        lambda c: '狼' if c in WOLF_WIN_CAMPS else '好人'

    )

    counts = (

        events.groupby(['姓名', '_model_target', '_side_label'], as_index=False)

        .size()

        .rename(columns={'size': '_cnt'})

    )

    def format_mixed_blood_records(group):

        ordered = group.sort_values(

            ['_cnt', '_model_target', '_side_label'],

            ascending=[False, True, True],

        )

        return '、'.join(

            f"{row['_model_target']}（{row['_side_label']}，{int(row['_cnt'])}）"

            for _, row in ordered.iterrows()

        )

    return (

        counts.groupby('姓名')

        .apply(format_mixed_blood_records, include_groups=False)

        .reset_index(name='混血儿记录')

    )



def summarize_prophet_first_check_players(data):

    """预言家/通灵师身份的 D1夜目标1，按姓名汇总为首验目标：姓名（次数）、…"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '首验': pd.Series(dtype=str)})

    if NIGHT_TARGET1_COL not in data.columns:

        return empty

    checks = data.loc[

        data['身份'].isin(PROPHET_FIRST_CHECK_ROLES),

        ['姓名', NIGHT_TARGET1_COL],

    ].dropna(subset=[NIGHT_TARGET1_COL])

    checks[NIGHT_TARGET1_COL] = checks[NIGHT_TARGET1_COL].astype(str).str.strip()

    checks = checks[checks[NIGHT_TARGET1_COL] != '']

    if checks.empty:

        return empty

    def format_target_counts(series):

        counts = series.value_counts()

        return '、'.join(

            f'{name}（{int(cnt)}）'

            for name, cnt in counts.sort_values(ascending=False).items()

        )

    return (

        checks.groupby('姓名')[NIGHT_TARGET1_COL]

        .apply(format_target_counts)

        .reset_index(name='首验')

    )



def summarize_first_checked_by(data):

    """被首验：按目标汇总首验自己的预言家/通灵师姓名（次数）。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '被首验': pd.Series(dtype=str)})

    game_keys = ['日期', '版型']

    if NIGHT_TARGET1_COL not in data.columns:

        return empty

    checks = data.loc[

        data['身份'].isin(PROPHET_FIRST_CHECK_ROLES),

        [*game_keys, '姓名', NIGHT_TARGET1_COL],

    ].copy()

    checks[NIGHT_TARGET1_COL] = checks[NIGHT_TARGET1_COL].astype(str).str.strip()

    checks = checks[checks[NIGHT_TARGET1_COL] != '']

    if checks.empty:

        return empty

    events = (

        checks.rename(columns={'姓名': '_首验者', NIGHT_TARGET1_COL: '姓名'})

        .drop_duplicates(subset=[*game_keys, '姓名', '_首验者'])

    )

    def format_checker_counts(series):

        counts = series.value_counts()

        return '、'.join(

            f'{name}（{int(cnt)}）'

            for name, cnt in counts.sort_values(ascending=False).items()

        )

    return (

        events.groupby('姓名')['_首验者']

        .apply(format_checker_counts)

        .reset_index(name='被首验')

    )



def _format_game_entry(row):

    date = row['日期']

    banxing = '' if pd.isna(row['版型']) else str(row['版型']).strip()

    identity = '' if pd.isna(row['身份']) else str(row['身份']).strip()

    return f'{date}（{banxing}，{identity}）'



def summarize_player_game_lists(data):

    """按姓名汇总参与/胜利场次明细：日期（版型，身份）、…"""

    empty = pd.DataFrame({

        '姓名': pd.Series(dtype=str),

        '参与场次': pd.Series(dtype=str),

        '胜利场次': pd.Series(dtype=str),

    })

    if '日期' not in data.columns:

        return empty

    def join_entries(group):

        if group.empty:

            return ''

        ordered = group.sort_values('日期', ascending=False)

        return '、'.join(_format_game_entry(row) for _, row in ordered.iterrows())

    participation = (

        data.groupby('姓名', group_keys=False)

        .apply(join_entries, include_groups=False)

        .reset_index(name='参与场次')

    )

    win_rows = data[data['胜利'].isin(['狼', '好人'])]

    if win_rows.empty:

        participation['胜利场次'] = ''

        return participation

    wins = (

        win_rows.groupby('姓名', group_keys=False)

        .apply(join_entries, include_groups=False)

        .reset_index(name='胜利场次')

    )

    return participation.merge(wins, on='姓名', how='left')



def assign_seat_numbers(data):

    """每局按行顺序依次为 1 号位起，写入「座位号」列。"""

    game_keys = ['日期', '版型']

    data = data.copy()

    data['座位号'] = data.groupby(game_keys, sort=False).cumcount() + 1

    return data



def summarize_seat_number_counts(data):

    """按姓名汇总各座位号出场次数：1号（次数）、2号（次数）、…"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '座位号次数': pd.Series(dtype=str)})

    game_keys = ['日期', '版型']

    required = [*game_keys, '姓名']

    if not all(col in data.columns for col in required):

        return empty

    frame = assign_seat_numbers(data[required])

    def format_seat_counts(seats):

        counts = seats.value_counts().sort_index()

        return '、'.join(

            f'{int(seat)}号（{int(cnt)}）'

            for seat, cnt in counts.items()

        )

    return (

        frame.groupby('姓名')['座位号']

        .apply(format_seat_counts)

        .reset_index(name='座位号次数')

    )



def build_seat_number_stats(data):

    """按姓名×座位号汇总场次、狼/好人胜率及警徽/放逐票指标。"""

    columns = [

        '姓名', '座位号', '场次', '狼人次数', '狼人胜率', '好人次数', '好人胜率',

        '警徽票次数', '警徽票正确率', '放逐票次数', '放逐票正确率',

    ]

    required = {

        '日期', '版型', '姓名', '狼标记', '狼胜利标记', '好人标记', '好人胜利标记',

        '警徽票标记', '警徽票正确标记', '放逐票次数', '正确放逐票',

    }

    if not required.issubset(data.columns):

        return pd.DataFrame(columns=columns)

    frame = assign_seat_numbers(data)

    stat = frame.groupby(['姓名', '座位号'], as_index=False).agg(

        场次=('姓名', 'count'),

        狼人次数=('狼标记', 'sum'),

        狼胜利次数=('狼胜利标记', 'sum'),

        好人次数=('好人标记', 'sum'),

        好人胜利次数=('好人胜利标记', 'sum'),

        警徽票次数=('警徽票标记', 'sum'),

        警徽票正确次数=('警徽票正确标记', 'sum'),

        放逐票次数=('放逐票次数', 'sum'),

        正确放逐票次数=('正确放逐票', 'sum'),

    )

    stat['狼人胜率'] = (

        stat['狼胜利次数'] / stat['狼人次数'].replace(0, pd.NA)

    ).fillna(0)

    stat['好人胜率'] = (

        stat['好人胜利次数'] / stat['好人次数'].replace(0, pd.NA)

    ).fillna(0)

    stat['警徽票正确率'] = (

        stat['警徽票正确次数'] / stat['警徽票次数'].replace(0, pd.NA)

    ).fillna(0)

    stat['放逐票正确率'] = (

        stat['正确放逐票次数'] / stat['放逐票次数'].replace(0, pd.NA)

    ).fillna(0)

    stat = stat.drop(

        columns=['狼胜利次数', '好人胜利次数', '警徽票正确次数', '正确放逐票次数']

    )

    rate_cols = ['狼人胜率', '好人胜率', '警徽票正确率', '放逐票正确率']

    stat[rate_cols] = stat[rate_cols].map(lambda x: f'{x:.1%}')

    count_cols = [

        '场次', '狼人次数', '好人次数', '警徽票次数', '放逐票次数',

    ]

    stat[count_cols] = stat[count_cols].astype(int)

    return stat[columns].sort_values(['姓名', '座位号']).reset_index(drop=True)



def assign_dream_first_wolf_markers(data):

    """摄梦人 D1夜目标1：非好人计首摄狼人；狼王/盗宝猎人计首摄狼王/盗宝猎人。"""

    game_keys = ['日期', '版型']

    data['首摄狼人标记'] = 0

    data['首摄狼王盗宝猎人标记'] = 0

    if NIGHT_TARGET1_COL not in data.columns:

        return data

    player_lookup = (

        data[game_keys + ['姓名', '身份']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': '_首摄目标', '身份': '_首摄目标身份'})

    )

    is_dreamer = data['身份'] == '摄梦人'

    target = data[NIGHT_TARGET1_COL].astype('string').str.strip()

    has_target = (

        is_dreamer

        & data[NIGHT_TARGET1_COL].notna()

        & (target != '')

        & (target != '<NA>')

    )

    if not has_target.any():

        return data

    tmp = (

        data.loc[has_target, game_keys + [NIGHT_TARGET1_COL]]

        .rename(columns={NIGHT_TARGET1_COL: '_首摄目标'})

        .merge(player_lookup, on=game_keys + ['_首摄目标'], how='left')

    )

    target_identity = tmp['_首摄目标身份'].astype('string').str.strip()

    has_identity = tmp['_首摄目标身份'].notna() & (target_identity != '') & (target_identity != '<NA>')

    is_non_good = has_identity & ~tmp['_首摄目标身份'].isin(GOOD_IDENTITIES)

    is_special = has_identity & tmp['_首摄目标身份'].isin(DREAM_FIRST_SPECIAL_IDENTITIES)

    data.loc[has_target, '首摄狼人标记'] = is_non_good.astype(int).values

    data.loc[has_target, '首摄狼王盗宝猎人标记'] = is_special.astype(int).values

    return data



def _get_d1_check_result_col(data):

    if D1_CHECK_RESULT_COL in data.columns:

        return D1_CHECK_RESULT_COL

    if D1_CHECK_RESULT_COL_LEGACY in data.columns:

        return D1_CHECK_RESULT_COL_LEGACY

    return None



def _get_fake_gold_events(data):

    """悍跳发假金事件：日期、版型、发假金玩家（A）、姓名（B）。"""

    game_keys = ['日期', '版型']

    check_col = 'D1验人'

    result_col = _get_d1_check_result_col(data)

    wolf_camps = {'狼人', '狼人混'}

    empty = pd.DataFrame(columns=[*game_keys, '_发假金玩家', '姓名'])

    if check_col not in data.columns or result_col is None:

        return empty

    is_wolf = data['阵营'].isin(wolf_camps)

    jumps = data.loc[

        is_wolf & data[check_col].notna(),

        [*game_keys, '姓名', check_col, result_col],

    ].copy()

    jumps[check_col] = jumps[check_col].astype(str).str.strip()

    jumps = jumps[jumps[check_col] != '']

    jumps[result_col] = jumps[result_col].astype(str).str.strip()

    jumps = jumps[jumps[result_col] != '查杀']

    if jumps.empty:

        return empty

    player_lookup = (

        data[game_keys + ['姓名', '阵营']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': check_col, '阵营': '_假金目标阵营'})

    )

    jumps = jumps.merge(player_lookup, on=game_keys + [check_col], how='left')

    target_camp = jumps['_假金目标阵营'].astype('string').str.strip()

    has_camp = jumps['_假金目标阵营'].notna() & (target_camp != '') & (target_camp != '<NA>')

    jumps = jumps[has_camp & ~jumps['_假金目标阵营'].isin(wolf_camps)]

    if jumps.empty:

        return empty

    return (

        jumps.rename(columns={'姓名': '_发假金玩家', check_col: '姓名'})

        .drop_duplicates(subset=[*game_keys, '姓名', '_发假金玩家'])

        .loc[:, [*game_keys, '_发假金玩家', '姓名']]

    )



def _poison_use_mask(data):

    """女巫/毒师且列名含「夜目标1」的任一格有非「救」的有效值。"""

    night_target_cols = [c for c in data.columns if '夜目标1' in c]

    if not night_target_cols:

        return pd.Series(False, index=data.index)

    is_poison_role = data['身份'].isin(POISON_ROLES)

    used_poison = pd.Series(False, index=data.index)

    for col in night_target_cols:

        target = data[col].astype('string').str.strip()

        col_used = (

            data[col].notna()

            & (target != '')

            & (target != '<NA>')

            & (target != BLIND_POISON_SAVE_MARK)

        )

        used_poison = used_poison | col_used

    return is_poison_role & used_poison



def _suppress_poison_mask(data):

    """女巫/毒师且所有含「夜目标1」的列均为空或「救」。"""

    night_target_cols = [c for c in data.columns if '夜目标1' in c]

    is_poison_role = data['身份'].isin(POISON_ROLES)

    if not night_target_cols:

        return is_poison_role

    suppressed = pd.Series(True, index=data.index)

    for col in night_target_cols:

        target = data[col].astype('string').str.strip()

        is_empty_or_save = (

            data[col].isna()

            | (target == '')

            | (target == '<NA>')

            | (target == BLIND_POISON_SAVE_MARK)

        )

        suppressed &= is_empty_or_save

    return is_poison_role & suppressed



def _poison_wolf_mask(data):

    """有毒药使用标记且任一夜目标1非「救」目标阵营为狼人。"""

    has_poison_use = _poison_use_mask(data)

    if not has_poison_use.any():

        return pd.Series(False, index=data.index)

    game_keys = ['日期', '版型']

    night_target_cols = [c for c in data.columns if '夜目标1' in c]

    if not night_target_cols:

        return pd.Series(False, index=data.index)

    lookup = (

        data[game_keys + ['姓名', '阵营']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': '_poison_target', '阵营': '_poison_target_camp'})

    )

    poison_wolf = pd.Series(False, index=data.index)

    for col in night_target_cols:

        target = data[col].astype('string').str.strip()

        col_valid = (

            has_poison_use

            & data[col].notna()

            & (target != '')

            & (target != '<NA>')

            & (target != BLIND_POISON_SAVE_MARK)

        )

        if not col_valid.any():

            continue

        frame = (

            data.loc[col_valid, game_keys + [col]]

            .rename(columns={col: '_poison_target'})

        )

        merged = frame.merge(lookup, on=game_keys + ['_poison_target'], how='left')

        wolf_hit = _is_blind_poison_wolf_camp(merged['_poison_target_camp']).to_numpy()

        poison_wolf.loc[frame.index[wolf_hit]] = True

    return poison_wolf



def _blind_poison_mask(data):

    """女巫/毒师且 D1夜目标1 非空且非「救」。"""

    if NIGHT_TARGET1_COL not in data.columns:

        return pd.Series(False, index=data.index)

    target = data[NIGHT_TARGET1_COL].astype('string').str.strip()

    return (

        data['身份'].isin(POISON_ROLES)

        & data[NIGHT_TARGET1_COL].notna()

        & (target != '')

        & (target != '<NA>')

        & (target != BLIND_POISON_SAVE_MARK)

    )



def _get_blind_poison_events(data):

    """盲毒事件：日期、版型、用毒者、盲毒目标。"""

    game_keys = ['日期', '版型']

    empty = pd.DataFrame(columns=[*game_keys, '姓名', '_盲毒目标'])

    has_blind = _blind_poison_mask(data)

    if not has_blind.any():

        return empty

    return (

        data.loc[has_blind, [*game_keys, '姓名', NIGHT_TARGET1_COL]]

        .rename(columns={NIGHT_TARGET1_COL: '_盲毒目标'})

        .assign(_盲毒目标=lambda df: df['_盲毒目标'].astype(str).str.strip())

    )



def _attach_blind_poison_target_camp(data, frame, target_col):

    """为盲毒目标补充同局玩家阵营。"""

    game_keys = ['日期', '版型']

    lookup = (

        data[game_keys + ['姓名', '阵营']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': target_col, '阵营': '_盲毒目标阵营'})

    )

    return frame.merge(lookup, on=game_keys + [target_col], how='left')



def _is_blind_poison_wolf_camp(series):

    camp = series.astype('string').str.strip()

    return series.notna() & (camp != '') & (camp != '<NA>') & camp.isin(BLIND_POISON_WOLF_CAMPS)



def _get_blind_poison_wolf_events(data):

    """盲毒且 D1夜目标1 对应玩家阵营为狼人的事件。"""

    events = _get_blind_poison_events(data)

    if events.empty:

        return events

    game_keys = ['日期', '版型']

    events = _attach_blind_poison_target_camp(data, events, '_盲毒目标')

    return events[_is_blind_poison_wolf_camp(events['_盲毒目标阵营'])].loc[

        :, [*game_keys, '姓名', '_盲毒目标']

    ]



def assign_blind_poison_markers(data):

    """女巫/毒师 D1夜目标1 非空且非「救」记盲毒；目标阵营为狼人记盲毒狼人。"""

    data['盲毒标记'] = 0

    data['盲毒狼人标记'] = 0

    has_blind = _blind_poison_mask(data)

    data.loc[has_blind, '盲毒标记'] = 1

    if not has_blind.any():

        return data

    game_keys = ['日期', '版型']

    tmp = _attach_blind_poison_target_camp(

        data,

        data.loc[has_blind, game_keys + [NIGHT_TARGET1_COL]],

        NIGHT_TARGET1_COL,

    )

    data.loc[has_blind, '盲毒狼人标记'] = _is_blind_poison_wolf_camp(tmp['_盲毒目标阵营']).astype(int).values

    return data



def summarize_blind_poison_wolves(data):

    """盲毒狼人：按女巫/毒师汇总盲毒到的狼人姓名（次数）。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '盲毒狼人': pd.Series(dtype=str)})

    events = _get_blind_poison_wolf_events(data)

    if events.empty:

        return empty

    game_keys = ['日期', '版型']

    events = events.drop_duplicates(subset=[*game_keys, '姓名', '_盲毒目标'])

    def format_wolf_counts(series):

        counts = series.value_counts()

        return '、'.join(

            f'{name}（{int(cnt)}）'

            for name, cnt in counts.sort_values(ascending=False).items()

        )

    return (

        events.groupby('姓名')['_盲毒目标']

        .apply(format_wolf_counts)

        .reset_index(name='盲毒狼人')

    )



def _get_poison_record_events(data):

    """毒药使用事件：日期、版型、女巫/毒师姓名、毒药目标姓名。"""

    game_keys = ['日期', '版型']

    empty = pd.DataFrame(columns=[*game_keys, '姓名', '_poison_target'])

    if '毒药使用标记' in data.columns:

        has_poison = data['毒药使用标记'] == 1

    else:

        has_poison = _poison_use_mask(data)

    if not has_poison.any():

        return empty

    night_target_cols = [c for c in data.columns if '夜目标1' in c]

    if not night_target_cols:

        return empty

    frames = []

    for col in night_target_cols:

        target = data[col].astype('string').str.strip()

        col_valid = (

            has_poison

            & data[col].notna()

            & (target != '')

            & (target != '<NA>')

            & (target != BLIND_POISON_SAVE_MARK)

        )

        if not col_valid.any():

            continue

        frame = (

            data.loc[col_valid, [*game_keys, '姓名', col]]

            .rename(columns={col: '_poison_target'})

            .assign(_poison_col=col)

        )

        frames.append(frame)

    if not frames:

        return empty

    return pd.concat(frames, ignore_index=True).drop_duplicates(

        subset=[*game_keys, '姓名', '_poison_target', '_poison_col']

    ).drop(columns=['_poison_col'])



def summarize_poison_records(data):

    """毒药记录：按女巫/毒师汇总毒药目标身份（次数）。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '毒药记录': pd.Series(dtype=str)})

    events = _get_poison_record_events(data)

    if events.empty:

        return empty

    game_keys = ['日期', '版型']

    lookup = (

        data[game_keys + ['姓名', '身份']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': '_poison_target', '身份': '_poison_target_identity'})

    )

    events = events.merge(lookup, on=game_keys + ['_poison_target'], how='left')

    identity = events['_poison_target_identity'].astype('string').str.strip()

    events = events[events['_poison_target_identity'].notna() & (identity != '') & (identity != '<NA>')]

    if events.empty:

        return empty

    def format_identity_counts(series):

        counts = series.value_counts()

        return '、'.join(

            f'{name}（{int(cnt)}）'

            for name, cnt in counts.sort_values(ascending=False).items()

        )

    return (

        events.groupby('姓名')['_poison_target_identity']

        .apply(format_identity_counts)

        .reset_index(name='毒药记录')

    )



def _skill_cols(data):

    return [c for c in data.columns if '技能' in c]



def _get_hunter_skill_events(data):

    """猎人技能事件：含「技能」列的有效目标姓名。"""

    game_keys = ['日期', '版型']

    empty = pd.DataFrame(

        columns=[*game_keys, '姓名', '_skill_target', '_skill_col', '_src_idx']

    )

    skill_cols = _skill_cols(data)

    if not skill_cols or '身份' not in data.columns:

        return empty

    is_hunter = data['身份'].astype('string').str.strip() == HUNTER_ROLE

    if not is_hunter.any():

        return empty

    frames = []

    for col in skill_cols:

        target = data[col].astype('string').str.strip()

        col_valid = (

            is_hunter

            & data[col].notna()

            & (target != '')

            & (target != '<NA>')

            & ~target.isin(HUNTER_SKILL_INVALID_MARKS)

        )

        if not col_valid.any():

            continue

        frame = data.loc[col_valid, game_keys + ['姓名']].copy()

        frame['_skill_target'] = target[col_valid].values

        frame['_skill_col'] = col

        frame['_src_idx'] = frame.index

        frames.append(frame)

    if not frames:

        return empty

    events = pd.concat(frames, ignore_index=True)

    return events.drop_duplicates(

        subset=[*game_keys, '姓名', '_skill_target', '_skill_col']

    )



def _attach_hunter_skill_target_info(data, events):

    """为猎人技能目标补充同局玩家阵营与身份。"""

    game_keys = ['日期', '版型']

    lookup = (

        data[game_keys + ['姓名', '阵营', '身份']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={

            '姓名': '_skill_target',

            '阵营': '_target_camp',

            '身份': '_target_identity',

        })

    )

    merged = events.merge(lookup, on=game_keys + ['_skill_target'], how='left')

    camp = merged['_target_camp'].astype('string').str.strip()

    identity = merged['_target_identity'].astype('string').str.strip()

    has_match = (

        merged['_target_camp'].notna()

        & (camp != '')

        & (camp != '<NA>')

        & merged['_target_identity'].notna()

        & (identity != '')

        & (identity != '<NA>')

    )

    return merged.loc[has_match]



def assign_hunter_skill_markers(data):

    """猎人：含「技能」列有效目标计技能次数，目标阵营为狼人计狼人次数。"""

    data['猎人技能次数'] = 0

    data['猎人技能狼人次数'] = 0

    events = _get_hunter_skill_events(data)

    if events.empty:

        return data

    matched = _attach_hunter_skill_target_info(data, events)

    if matched.empty:

        return data

    for idx, grp in matched.groupby('_src_idx'):

        data.loc[idx, '猎人技能次数'] = len(grp)

        wolf_hit = grp['_target_camp'].astype('string').str.strip().isin(HUNTER_SKILL_WOLF_CAMPS)

        data.loc[idx, '猎人技能狼人次数'] = int(wolf_hit.sum())

    return data



def summarize_hunter_skill_records(data):

    """猎人技能记录：按猎人汇总技能目标身份（次数）。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '猎人技能记录': pd.Series(dtype=str)})

    events = _get_hunter_skill_events(data)

    if events.empty:

        return empty

    matched = _attach_hunter_skill_target_info(data, events)

    if matched.empty:

        return empty

    def format_identity_counts(series):

        counts = series.value_counts()

        return '、'.join(

            f'{name}（{int(cnt)}）'

            for name, cnt in counts.sort_values(ascending=False).items()

        )

    return (

        matched.groupby('姓名')['_target_identity']

        .apply(format_identity_counts)

        .reset_index(name='猎人技能记录')

    )



def assign_lagan_markers(data):

    """通灵师场次中，悍跳狼 D1验人结果非金水/查杀记拉杆；验人目标身份与结果一致记拉杆成功。"""

    game_keys = ['日期', '版型']

    check_col = 'D1验人'

    result_col = _get_d1_check_result_col(data)

    data['拉杆标记'] = 0

    data['拉杆成功标记'] = 0

    if check_col not in data.columns or result_col is None:

        return data

    tl_games = (

        data.loc[data['身份'] == '通灵师', game_keys]

        .drop_duplicates()

    )

    if tl_games.empty:

        return data

    result_text = data[result_col].astype('string').str.strip()

    lagan_mask = (

        (data['悍跳标记'] == 1)

        & _is_filled_value(data[check_col])

        & _is_filled_value(data[result_col])

        & ~result_text.isin(['金水', '查杀'])

    )

    lagan_rows = data.loc[lagan_mask, game_keys].drop_duplicates()

    lagan_rows = lagan_rows.merge(tl_games.assign(_has_tl=1), on=game_keys, how='inner')

    if lagan_rows.empty:

        return data

    hit = data[game_keys].merge(

        lagan_rows[game_keys].assign(_lagan=1),

        on=game_keys,

        how='left',

    )['_lagan'].fillna(0).astype(bool)

    data.loc[lagan_mask & hit, '拉杆标记'] = 1

    frame = data.loc[data['拉杆标记'] == 1, game_keys + ['姓名', check_col, result_col]].copy()

    player_lookup = (

        data[game_keys + ['姓名', '身份']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': check_col, '身份': '_验人目标身份'})

    )

    merged = frame.merge(player_lookup, on=game_keys + [check_col], how='left')

    merged.index = frame.index

    target_id = merged['_验人目标身份'].astype('string').str.strip()

    claimed = merged[result_col].astype('string').str.strip()

    success_mask = (

        target_id.notna()

        & (target_id != '')

        & (target_id != '<NA>')

        & (target_id == claimed)

    )

    data.loc[frame.index[success_mask.to_numpy()], '拉杆成功标记'] = 1

    return data



def _format_lagan_record(row, check_col, result_col):

    """单条拉杆成功记录：日期-姓名-D1验人-D1验人结果。"""

    def cell_text(val):

        if val is None or (isinstance(val, float) and pd.isna(val)):

            return ''

        text = str(val).strip()

        return '' if text in ('', 'nan', 'None', '<NA>') else text

    check = cell_text(row[check_col])

    result = cell_text(row[result_col])

    if not check or not result:

        return ''

    return f"{row['日期']}-{row['姓名']}-{check}-{result}"



def summarize_lagan_records(data):

    """拉杆成功记录：按拉杆成功玩家汇总，多条用逗号连接。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '拉杆记录': pd.Series(dtype=str)})

    check_col = 'D1验人'

    result_col = _get_d1_check_result_col(data)

    if '拉杆成功标记' not in data.columns or result_col is None:

        return empty

    hits = data.loc[

        data['拉杆成功标记'] == 1,

        ['姓名', '日期', check_col, result_col],

    ].copy()

    if hits.empty:

        return empty

    hits['_record'] = hits.apply(

        lambda row: _format_lagan_record(row, check_col, result_col),

        axis=1,

    )

    hits = hits[hits['_record'] != '']

    if hits.empty:

        return empty

    return (

        hits.sort_values('日期', ascending=False)

        .groupby('姓名', as_index=False)['_record']

        .agg(lambda records: ','.join(records))

        .rename(columns={'_record': '拉杆记录'})

    )



def _join_unique_names(names):

    ordered = []

    seen = set()

    for name in names:

        text = str(name).strip()

        if not text or text in ('', '<NA>', 'nan', 'None'):

            continue

        if text not in seen:

            seen.add(text)

            ordered.append(text)

    return '、'.join(ordered)



def assign_prophet_replaced_jump_markers(data):

    """预通被代跳：真预/通灵未验人，同局有好人侧 D1验人 有值。"""

    check_col = 'D1验人'

    game_keys = ['日期', '版型']

    data['预通被代跳标记'] = 0

    if check_col not in data.columns:

        return data

    role = data['身份']

    is_prophet = role.isin(PROPHET_FIRST_CHECK_ROLES)

    is_good = ~data['阵营'].isin(['狼人', '狼人混'])

    prophet_no_check = is_prophet & ~_is_filled_value(data[check_col])

    game_has_good_check = (

        data.assign(_good_check=(is_good & _is_filled_value(data[check_col])).astype(int))

        .groupby(game_keys)['_good_check']

        .transform('max')

        .gt(0)

    )

    data['预通被代跳标记'] = (

        prophet_no_check & game_has_good_check

    ).fillna(False).astype(int)

    return data



def summarize_prophet_didi_records(data):

    """预通滴滴记录：被代跳局中，同局 D1验人 有值的好人姓名（顿号连接）。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '预通滴滴记录': pd.Series(dtype=str)})

    check_col = 'D1验人'

    game_keys = ['日期', '版型']

    if '预通被代跳标记' not in data.columns or check_col not in data.columns:

        return empty

    is_good = ~data['阵营'].isin(['狼人', '狼人混'])

    check_filled = _is_filled_value(data[check_col])

    prophets = data.loc[

        data['预通被代跳标记'] == 1,

        ['姓名', *game_keys],

    ].drop_duplicates()

    if prophets.empty:

        return empty

    jumpers = (

        data.loc[is_good & check_filled, [*game_keys, '姓名']]

        .drop_duplicates(subset=[*game_keys, '姓名'])

        .rename(columns={'姓名': '_jumper'})

    )

    events = prophets.merge(jumpers, on=game_keys, how='inner')

    if events.empty:

        return empty

    events = events.sort_values([*game_keys, '_jumper'])

    rows = []

    for name, group in events.groupby('姓名', sort=False):

        rows.append({

            '姓名': name,

            '预通滴滴记录': _join_unique_names(group['_jumper'].tolist()),

        })

    return pd.DataFrame(rows)



def _pick_prophet_name_for_game(game):

    """同对局预言家/通灵师姓名（优先起跳预言家标记）。"""

    prophets = game.loc[game['身份'].isin(PROPHET_FIRST_CHECK_ROLES)]

    if prophets.empty:

        return ''

    jump = prophets.loc[prophets['起跳预言家标记'] == 1, '姓名']

    if not jump.empty:

        return str(jump.iloc[0]).strip()

    return str(prophets['姓名'].iloc[0]).strip()



def _pick_hanjump_name_for_game(game):

    """同对局悍跳狼姓名。"""

    jumps = game.loc[game['悍跳标记'] == 1, '姓名']

    if jumps.empty:

        return ''

    return str(jumps.iloc[0]).strip()



def summarize_sheriff_vote_error_records(data):

    """警上站狼边：有警徽票标记且无警徽票正确标记时，汇总「预言家/通灵师-悍跳狼」。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '警上站狼边': pd.Series(dtype=str)})

    required = {

        '警徽票标记', '警徽票正确标记', '起跳预言家标记', '悍跳标记',

        '身份', '日期', '版型', '姓名',

    }

    if not required.issubset(data.columns):

        return empty

    hits = data.loc[

        (data['警徽票标记'] > 0) & (data['警徽票正确标记'] == 0),

        ['姓名', '日期', '版型'],

    ].copy()

    if hits.empty:

        return empty

    game_keys = ['日期', '版型']

    pair_map = {}

    for key, game in data.groupby(game_keys, sort=False):

        prophet = _pick_prophet_name_for_game(game)

        hanjump = _pick_hanjump_name_for_game(game)

        pair_map[key] = f'{prophet}-{hanjump}' if prophet and hanjump else ''

    hits['_record'] = hits.apply(

        lambda row: pair_map.get((row['日期'], row['版型']), ''),

        axis=1,

    )

    hits = hits[hits['_record'] != '']

    if hits.empty:

        return empty

    return (

        hits.sort_values('日期', ascending=False)

        .groupby('姓名', as_index=False)['_record']

        .agg(lambda records: ','.join(records))

        .rename(columns={'_record': '警上站狼边'})

    )



def assign_fake_gold_markers(data):

    """悍跳狼发假金时，被验玩家阵营非狼人/狼人混则记假金标记。"""

    game_keys = ['日期', '版型']

    events = _get_fake_gold_events(data)

    if events.empty:

        data['假金标记'] = 0

        return data

    targets = (

        events.drop_duplicates(subset=[*game_keys, '姓名'])

        .assign(假金标记=1)[game_keys + ['姓名', '假金标记']]

    )

    data = data.drop(columns=['假金标记'], errors='ignore')

    data = data.merge(targets, on=[*game_keys, '姓名'], how='left')

    data['假金标记'] = data['假金标记'].fillna(0).astype(int)

    return data



def summarize_fake_gold_givers(data):

    """被发假金玩家：按目标汇总发假金的悍跳狼人姓名（次数）。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '接狼人金水': pd.Series(dtype=str)})

    events = _get_fake_gold_events(data)

    if events.empty:

        return empty

    def format_giver_counts(series):

        counts = series.value_counts()

        return '、'.join(

            f'{name}（{int(cnt)}）'

            for name, cnt in counts.sort_values(ascending=False).items()

        )

    return (

        events.groupby('姓名')['_发假金玩家']

        .apply(format_giver_counts)

        .reset_index(name='接狼人金水')

    )



def _summarize_dimension_win_rates(data, dimension_col, result_col):

    """按玩家汇总指定维度（身份/版型等）的出场次数与胜率。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), result_col: pd.Series(dtype=str)})

    required = {'姓名', dimension_col, '胜利标记'}

    if not required.issubset(data.columns):

        return empty

    events = data[['姓名', dimension_col, '胜利标记']].copy()

    events[dimension_col] = events[dimension_col].astype('string').str.strip()

    events = events[

        events[dimension_col].notna()

        & (events[dimension_col] != '')

        & (events[dimension_col] != '<NA>')

    ]

    if events.empty:

        return empty

    grouped = (

        events.groupby(['姓名', dimension_col], as_index=False)

        .agg(场次=('胜利标记', 'count'), 胜场=('胜利标记', 'sum'))

    )

    grouped['胜率'] = grouped['胜场'] / grouped['场次'].replace(0, pd.NA)

    rows = []

    for name, group in grouped.groupby('姓名', sort=False):

        ordered = group.sort_values(['场次', dimension_col], ascending=[False, True])

        rows.append({

            '姓名': name,

            result_col: '、'.join(

                f"{row[dimension_col]}（{int(row['场次'])}次，{row['胜率']:.1%}）"

                for _, row in ordered.iterrows()

            ),

        })

    return pd.DataFrame(rows)



def summarize_identity_win_rates(data):

    """按玩家汇总各身份出场次数与胜率。"""

    return _summarize_dimension_win_rates(data, '身份', '身份胜率')



def summarize_banxing_win_rates(data):

    """按玩家汇总各版型出场次数与胜率。"""

    return _summarize_dimension_win_rates(data, '版型', '版型胜率')



def _summarize_dimension_wolf_rates(data, dimension_col, result_col):

    """按玩家汇总指定维度（身份/版型等）的出场次数与狼人率。"""

    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), result_col: pd.Series(dtype=str)})

    required = {'姓名', dimension_col, '狼标记'}

    if not required.issubset(data.columns):

        return empty

    events = data[['姓名', dimension_col, '狼标记']].copy()

    events[dimension_col] = events[dimension_col].astype('string').str.strip()

    events = events[

        events[dimension_col].notna()

        & (events[dimension_col] != '')

        & (events[dimension_col] != '<NA>')

    ]

    if events.empty:

        return empty

    grouped = (

        events.groupby(['姓名', dimension_col], as_index=False)

        .agg(场次=('狼标记', 'count'), 狼场=('狼标记', 'sum'))

    )

    grouped['狼人率'] = grouped['狼场'] / grouped['场次'].replace(0, pd.NA)

    rows = []

    for name, group in grouped.groupby('姓名', sort=False):

        ordered = group.sort_values(['场次', dimension_col], ascending=[False, True])

        rows.append({

            '姓名': name,

            result_col: '、'.join(

                f"{row[dimension_col]}（{int(row['场次'])}次，{row['狼人率']:.1%}）"

                for _, row in ordered.iterrows()

            ),

        })

    return pd.DataFrame(rows)



def summarize_banxing_wolf_rates(data):

    """按玩家汇总各版型出场次数与狼人率。"""

    return _summarize_dimension_wolf_rates(data, '版型', '版型狼人率')



def _non_daobao_red_wolf_mask(data):

    """身份为狼/狼王/黑狼王/狼术师/狼美人/诡术师且版型非盗宝大师。"""

    banxing = data['版型'].astype('string').str.strip()

    return data['身份'].isin(RED_WOLF_IDENTITIES) & (banxing != DAOBAO_MASTER_BANXING)



def assign_red_wolf_knife_markers(data):

    """非盗宝红狼、自刀、狼队友自刀标记。"""

    data['非盗宝红狼标记'] = _non_daobao_red_wolf_mask(data).astype(int)

    data['自刀标记'] = 0

    data['狼队友自刀标记'] = 0

    if D1_WOLF_KNIFE_COL not in data.columns:

        return data

    is_red_wolf = _non_daobao_red_wolf_mask(data)

    knife = data[D1_WOLF_KNIFE_COL].astype('string').str.strip()

    name = data['姓名'].astype('string').str.strip()

    has_knife = (

        data[D1_WOLF_KNIFE_COL].notna()

        & (knife != '')

        & (knife != '<NA>')

    )

    data['自刀标记'] = (is_red_wolf & has_knife & (knife == name)).astype(int)

    teammate_mask = is_red_wolf & has_knife & (knife != name)

    if not teammate_mask.any():

        return data

    game_keys = ['日期', '版型']

    red_wolf_lookup = (

        data.loc[is_red_wolf, game_keys + ['姓名']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': '_d1_knife_target'})

        .assign(_is_red_wolf_target=1)

    )

    frame = (

        data.loc[teammate_mask, game_keys + [D1_WOLF_KNIFE_COL]]

        .rename(columns={D1_WOLF_KNIFE_COL: '_d1_knife_target'})

    )

    merged = frame.merge(red_wolf_lookup, on=game_keys + ['_d1_knife_target'], how='left')

    hit = merged['_is_red_wolf_target'].fillna(0).astype(bool).to_numpy()

    data.loc[frame.index[hit], '狼队友自刀标记'] = 1

    return data



def assign_first_knife_witch_markers(data):

    """狼人阵营玩家所在对局 D1狼刀 目标为女巫时记 1。"""

    data['首刀女巫标记'] = 0

    if D1_WOLF_KNIFE_COL not in data.columns:

        return data

    is_wolf = data['阵营'].isin(['狼人', '狼人混'])

    knife = data[D1_WOLF_KNIFE_COL].astype('string').str.strip()

    has_knife = (

        data[D1_WOLF_KNIFE_COL].notna()

        & (knife != '')

        & (knife != '<NA>')

    )

    wolf_knife_mask = is_wolf & has_knife

    if not wolf_knife_mask.any():

        return data

    game_keys = ['日期', '版型']

    witch_lookup = (

        data.loc[data['身份'] == '女巫', game_keys + ['姓名']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': '_d1_knife_target'})

        .assign(_is_witch_target=1)

    )

    frame = (

        data.loc[wolf_knife_mask, game_keys + [D1_WOLF_KNIFE_COL]]

        .rename(columns={D1_WOLF_KNIFE_COL: '_d1_knife_target'})

    )

    merged = frame.merge(witch_lookup, on=game_keys + ['_d1_knife_target'], how='left')

    hit = merged['_is_witch_target'].fillna(0).astype(bool).to_numpy()

    data.loc[frame.index[hit], '首刀女巫标记'] = 1

    return data



def _is_filled_value(series):

    text = series.astype('string').str.strip()

    return series.notna() & (text != '') & (text != '<NA>')



def _is_filled_scalar(val):

    if pd.isna(val):

        return False

    text = str(val).strip()

    return text != '' and text != '<NA>'



def _is_wolf_camp(camp):

    return camp in {'狼人', '狼人混'}



def _first_exile_day(player_row):

    """返回玩家状态首次为「被放逐」的天数（DAYS 元素），无则 None。"""

    for day in DAYS:

        state_col = f'D{day}状态'

        val = player_row.get(state_col)

        if _is_filled_scalar(val) and str(val).strip() == '被放逐':

            return day

    return None



def _prophet_medium_blocks_exile_day(player_row, day):

    """预言家/通灵师在该天是否导致不统计放逐票。"""

    state_col = f'D{day}状态'

    val = player_row.get(state_col)

    if not _is_filled_scalar(val):

        return True

    if str(val).strip() == '被放逐' and _first_exile_day(player_row) == day:

        return True

    return False



def _build_no_prophet_push_countable_lookup(data):

    """按对局+天数：无预通生推阶段是否可统计放逐票。"""

    game_keys = ['日期', '版型']

    prophet_roles = set(PROPHET_FIRST_CHECK_ROLES)

    records = []

    for (date, banxing), group in data.groupby(game_keys, sort=False):

        pm_players = group[group['身份'].isin(prophet_roles)]

        for day in DAYS:

            blocked = any(

                _prophet_medium_blocks_exile_day(prow, day)

                for _, prow in pm_players.iterrows()

            )

            records.append({

                '日期': date,

                '版型': banxing,

                'day': day,

                '无预通生推可统计': int(not blocked),

            })

    return pd.DataFrame(records)



def _assign_no_prophet_push_exile_markers(data):

    """无预通生推：排除预/通存活及被放逐当日的放逐票。"""

    lookup = _build_no_prophet_push_countable_lookup(data)

    if lookup.empty:

        data['无预通生推正确放逐票'] = 0

        data['无预通放逐票'] = 0

        return data

    lookup_wide = lookup.pivot(index=['日期', '版型'], columns='day', values='无预通生推可统计')

    lookup_wide = lookup_wide.reset_index()

    rename_map = {day: f'_无预通生推D{day}' for day in lookup_wide.columns if day not in ('日期', '版型')}

    lookup_wide = lookup_wide.rename(columns=rename_map)

    data = data.merge(lookup_wide, on=['日期', '版型'], how='left')

    correct_total = pd.Series(0, index=data.index, dtype=int)

    vote_total = pd.Series(0, index=data.index, dtype=int)

    for day in DAYS:

        day_flag = data[f'_无预通生推D{day}'].fillna(1).astype(int)

        for suffix in ['', '2']:

            vote_col = f'第{day}天放逐票标记{suffix}'

            correct_col = f'第{day}天正确逐票标记{suffix}'

            if vote_col in data.columns:

                vote_total = vote_total + data[vote_col] * day_flag

            if correct_col in data.columns:

                correct_total = correct_total + data[correct_col] * day_flag

    data['无预通生推正确放逐票'] = correct_total

    data['无预通放逐票'] = vote_total

    drop_cols = [c for c in data.columns if c.startswith('_无预通生推D')]

    return data.drop(columns=drop_cols)



def _assign_arcane_exile_correct_markers(data):

    """诡术之境：D{n}夜目标1/2 为一狼一好人时，D{n}放逐票1 或 D{n}放逐票2 投该好人均算正确。"""

    game_keys = ['日期', '版型']

    is_wolf_side = data['阵营'].isin(['狼人', '狼人混'])

    is_good = ~is_wolf_side

    role = data['身份']

    can_vote_exile = ~role.isin(['通灵师', '预言家'])

    in_arcane = data['版型'].astype(str).str.strip() == ARCANE_BANXING

    if not in_arcane.any():

        return data

    camp_base = data[game_keys + ['姓名', '阵营']].drop_duplicates(subset=game_keys + ['姓名'])

    good_targets = []

    master_rows = data.loc[in_arcane & (role == ARCANE_MASTER_ROLE)]

    for _, mrow in master_rows.iterrows():

        players = camp_base[

            (camp_base['日期'] == mrow['日期']) & (camp_base['版型'] == mrow['版型'])

        ]

        camp_of = players.set_index('姓名')['阵营'].to_dict()

        for day in DAYS:

            t1_col = f'D{day}夜目标1'

            t2_col = f'D{day}夜目标2'

            if t1_col not in data.columns or t2_col not in data.columns:

                continue

            a = mrow.get(t1_col)

            b = mrow.get(t2_col)

            if not (_is_filled_scalar(a) and _is_filled_scalar(b)):

                continue

            a, b = str(a).strip(), str(b).strip()

            if a == b or a not in camp_of or b not in camp_of:

                continue

            ca, cb = camp_of[a], camp_of[b]

            a_wolf = _is_wolf_camp(ca)

            b_wolf = _is_wolf_camp(cb)

            if a_wolf == b_wolf:

                continue

            good_target = b if a_wolf else a

            good_targets.append({

                '日期': mrow['日期'],

                '版型': mrow['版型'],

                'day': day,

                'good_target': good_target,

            })

    if not good_targets:

        return data

    gt_df = pd.DataFrame(good_targets)

    for day in DAYS:

        day_gt = gt_df[gt_df['day'] == day]

        if day_gt.empty:

            continue

        for n, suffix in [('1', ''), ('2', '2')]:

            vote_col = f'D{day}放逐票{n}'

            marker_col = f'第{day}天正确逐票标记{suffix}'

            if vote_col not in data.columns:

                continue

            lookup = (

                day_gt[game_keys + ['good_target']]

                .drop_duplicates(subset=game_keys)

                .rename(columns={'good_target': vote_col})

                .assign(_arcane_good=1)

            )

            vote_filled = in_arcane & is_good & _is_filled_value(data[vote_col]) & can_vote_exile

            if not vote_filled.any():

                continue

            frame = data.loc[vote_filled, game_keys + [vote_col]]

            merged = frame.merge(lookup, on=game_keys + [vote_col], how='left')

            hit = merged['_arcane_good'].fillna(0).astype(bool).to_numpy()

            data.loc[frame.index[hit], marker_col] = 1

    return data



def _get_second_sheriff_vote_col(data):

    if D1_SECOND_SHERIFF_VOTE_COL in data.columns:

        return D1_SECOND_SHERIFF_VOTE_COL

    return None



def _daobao_master_medium_sheriff_exclude_mask(data):

    """盗宝大师版型且局内含盗宝通灵师：不统计警徽票。"""

    game_keys = ['日期', '版型']

    required = {*game_keys, '身份', '版型'}

    if not required.issubset(data.columns):

        return pd.Series(False, index=data.index)

    banxing = data['版型'].astype('string').str.strip()

    role = data['身份'].astype('string').str.strip()

    exclude_games = (

        data.loc[

            (banxing == DAOBAO_MASTER_BANXING) & (role == DAOBAO_MEDIUM_ROLE),

            game_keys,

        ]

        .drop_duplicates()

        .assign(_exclude_sheriff=1)

    )

    if exclude_games.empty:

        return pd.Series(False, index=data.index)

    merged = data[game_keys].merge(exclude_games, on=game_keys, how='left')

    return merged['_exclude_sheriff'].fillna(0).astype(bool).to_numpy()



def assign_jump_prophet_markers(data):

    """起跳预言家：真预/通有验人，或好身份非预通验人且预通验人为空。"""

    game_keys = ['日期', '版型']

    role = data['身份']

    is_good = ~data['阵营'].isin(['狼人', '狼人混'])

    is_prophet_role = role.isin(PROPHET_FIRST_CHECK_ROLES)

    check_filled = _is_filled_value(data['D1验人'])

    data['起跳预言家标记'] = (is_prophet_role & check_filled).astype(int)

    prophet_rows = data.loc[is_prophet_role, game_keys + ['D1验人']]

    if prophet_rows.empty:

        return data

    prophet_check_empty = (

        prophet_rows.groupby(game_keys, as_index=False)

        .agg(_prophet_any_check=('D1验人', lambda s: _is_filled_value(s).any()))

    )

    prophet_check_empty['_prophet_all_empty'] = ~prophet_check_empty['_prophet_any_check']

    case1_base = is_good & ~is_prophet_role & check_filled

    if not case1_base.any():

        return data

    frame = data.loc[case1_base, game_keys]

    merged = frame.merge(

        prophet_check_empty[game_keys + ['_prophet_all_empty']],

        on=game_keys,

        how='left',

    )

    hit = merged['_prophet_all_empty'].fillna(False).to_numpy()

    data.loc[frame.index[hit], '起跳预言家标记'] = 1

    return data



def _assign_sheriff_vote_correct_marker(data, vote_col, marker_col, order_col=None, order_val=None):

    """好人警徽票投给起跳预言家则记正确。"""

    game_keys = ['日期', '版型']

    is_good = ~data['阵营'].isin(['狼人', '狼人混'])

    data[marker_col] = 0

    if vote_col is None or vote_col not in data.columns:

        return data

    jump_lookup = (

        data.loc[data['起跳预言家标记'] == 1, game_keys + ['姓名']]

        .drop_duplicates(subset=game_keys + ['姓名'])

        .rename(columns={'姓名': vote_col})

        .assign(_is_jump_prophet=1)

    )

    if jump_lookup.empty:

        return data

    vote_filled = is_good & _is_filled_value(data[vote_col])

    if order_col is not None:

        order = data[order_col].astype('string').str.strip()

        vote_filled = vote_filled & (order == order_val)

    if not vote_filled.any():

        return data

    frame = data.loc[vote_filled, game_keys + [vote_col]]

    merged = frame.merge(jump_lookup, on=game_keys + [vote_col], how='left')

    hit = merged['_is_jump_prophet'].fillna(0).astype(bool).to_numpy()

    data.loc[frame.index[hit], marker_col] = 1

    return data



def assign_prophet_medium_out_markers(data):

    """预通相关统计标记（按局）。"""

    role = data['身份']

    is_prophet = role.isin(PROPHET_FIRST_CHECK_ROLES)

    data['预通被放逐标记'] = 0

    data['预通被毒标记'] = 0

    data['预通被枪标记'] = 0

    data['预通获警徽标记'] = 0

    data['预通被奶死标记'] = 0

    data['预通被盲毒标记'] = 0



    state_cols = [col for col in data.columns if '状态' in col]

    if state_cols:

        states = data[state_cols].astype('string').apply(lambda series: series.str.strip())

        data['预通被放逐标记'] = (is_prophet & states.eq('被放逐').any(axis=1)).fillna(False).astype(int)

        data['预通被毒标记'] = (is_prophet & states.eq('被毒').any(axis=1)).fillna(False).astype(int)

        data['预通被枪标记'] = (is_prophet & states.eq('被枪').any(axis=1)).fillna(False).astype(int)

        data['预通被奶死标记'] = (is_prophet & states.eq('同守同救out').any(axis=1)).fillna(False).astype(int)



    if D1_STATE_COL in data.columns:

        d1_state = data[D1_STATE_COL].astype('string').str.strip()

        data['预通被盲毒标记'] = (is_prophet & d1_state.eq('被毒')).fillna(False).astype(int)



    if D1_SHERIFF_BADGE_COL in data.columns:

        name = data['姓名'].astype('string').str.strip()

        badge = data[D1_SHERIFF_BADGE_COL].astype('string').str.strip()

        badge_filled = badge.notna() & (badge != '') & (badge != '<NA>')

        data['预通获警徽标记'] = (is_prophet & badge_filled & badge.eq(name)).fillna(False).astype(int)



    return assign_prophet_replaced_jump_markers(data)



def add_markers(data):

    """生成玩家级统计标记列。"""

    is_wolf = data['阵营'].isin(['狼人', '狼人混'])

    is_good = ~is_wolf

    role = data['身份']

    data['胜利标记'] = data['胜利'].isin(['狼', '好人']).astype(int)

    data['狼标记'] = is_wolf.astype(int)

    data['技能狼标记'] = (

        (data['阵营'] == '狼人') & (role.astype('string').str.strip() != '狼')

    ).astype(int)

    data['身份标记'] = data['阵营'].isin(['神职', '狼人', '狼人混']).astype(int)

    data['预通标记'] = role.isin(['预言家', '通灵师']).astype(int)

    data = assign_prophet_medium_out_markers(data)

    data['神职身份标记'] = (data['阵营'] == '神职').astype(int)

    data['机械狼标记'] = role.isin(JIXIE_WOLF_ROLES).astype(int)

    for jixie_role in JIXIE_SUB_ROLES:

        data[f'{jixie_role}标记'] = (role == jixie_role).astype(int)

    data['好人标记'] = is_good.astype(int)

    data['好人胜利标记'] = (

        data['阵营'].isin(['平民', '神职']) & (data['胜利'] == '好人')

    ).astype(int)

    data = assign_survival_days(data)

    data['女巫毒师标记'] = role.isin(['女巫', '毒师']).astype(int)

    data['压毒标记'] = _suppress_poison_mask(data).astype(int)

    data['毒药使用标记'] = _poison_use_mask(data).astype(int)

    data['毒狼人标记'] = _poison_wolf_mask(data).astype(int)

    data['猎人标记'] = (role == '猎人').astype(int)

    data = assign_hunter_skill_markers(data)

    data['守卫标记'] = (role == '守卫').astype(int)

    data['摄梦人标记'] = (role == '摄梦人').astype(int)

    data['狼胜利标记'] = ((data['胜利'] == '狼') & is_wolf).astype(int)

    data = assign_jump_prophet_markers(data)

    data['警下标记'] = (is_good & (data['D1发言顺序'] == '警下')).astype(int)

    data = _assign_sheriff_vote_correct_marker(

        data,

        D1_SHERIFF_VOTE_COL,

        '第一轮警徽票正确标记',

        order_col='D1发言顺序',

        order_val='警下',

    )

    data = _assign_sheriff_vote_correct_marker(

        data,

        _get_second_sheriff_vote_col(data),

        '第二轮警徽票正确标记',

    )

    data['警徽票正确标记'] = (

        data['第一轮警徽票正确标记'] + data['第二轮警徽票正确标记']

    )

    first_sheriff_vote_count = (

        is_good & _is_filled_value(data[D1_SHERIFF_VOTE_COL])

    ).astype(int)

    second_vote_col = _get_second_sheriff_vote_col(data)

    if second_vote_col:

        data['警徽票标记'] = (

            first_sheriff_vote_count

            + (is_good & _is_filled_value(data[second_vote_col])).astype(int)

        )

    else:

        data['警徽票标记'] = first_sheriff_vote_count

    exclude_sheriff = _daobao_master_medium_sheriff_exclude_mask(data)

    if exclude_sheriff.any():

        for col in (

            '第一轮警徽票正确标记', '第二轮警徽票正确标记',

            '警徽票正确标记', '警徽票标记',

        ):

            data.loc[exclude_sheriff, col] = 0

    data['悍跳标记'] = (is_wolf & data['D1验人'].notna()).astype(int)

    data['自爆标记'] = (

        is_wolf & data[STATE_COLS].eq('自爆').any(axis=1)

    ).astype(int)

    data['被盲毒标记'] = (data['D1状态'] == '被毒').astype(int)

    data['非狼被盲毒标记'] = (

        (data['被盲毒标记'] == 1) & (data['阵营'] != '狼人')

    ).astype(int)

    can_vote_exile = ~role.isin(['通灵师', '预言家'])

    for day in DAYS:

        for n, suffix in [('1', ''), ('2', '2')]:

            vote = data[f'D{day}放逐票{n}']

            vote_filled = vote.notna() & (vote.astype(str).str.strip() != '')

            valid = is_good & vote_filled & can_vote_exile

            data[f'第{day}天放逐票标记{suffix}'] = valid.astype(int)

            data[f'第{day}天正确逐票标记{suffix}'] = (valid & (data[f'D{day}放逐票{n}阵营'] == '狼人')).astype(int)

    data = _assign_arcane_exile_correct_markers(data)

    if SPECIAL_ORDER_EXILE_COL in data.columns:

        special_vote = data[SPECIAL_ORDER_EXILE_COL]

        special_filled = special_vote.notna() & (special_vote.astype(str).str.strip() != '')

        special_valid = is_good & special_filled & can_vote_exile

        data['特殊放逐票标记'] = special_valid.astype(int)

        camp_col = f'{SPECIAL_ORDER_EXILE_COL}阵营'

        if camp_col in data.columns:

            data['特殊正确放逐票标记'] = (

                special_valid & (data[camp_col] == '狼人')

            ).astype(int)

        else:

            data['特殊正确放逐票标记'] = 0

    else:

        data['特殊放逐票标记'] = 0

        data['特殊正确放逐票标记'] = 0

    data = _assign_no_prophet_push_exile_markers(data)

    correct_cols = [f'第{d}天正确逐票标记' for d in DAYS] + [f'第{d}天正确逐票标记2' for d in DAYS] + ['特殊正确放逐票标记']

    vote_cols = [f'第{d}天放逐票标记' for d in DAYS] + [f'第{d}天放逐票标记2' for d in DAYS] + ['特殊放逐票标记']

    data['正确放逐票'] = data[correct_cols].sum(axis=1)

    data['放逐票次数'] = data[vote_cols].sum(axis=1)

    is_civilian = (role == '平民').astype(int)

    data['平民放逐票'] = data['放逐票次数'] * is_civilian

    data['平民正确放逐票'] = data['正确放逐票'] * is_civilian

    data['平民警徽票标记'] = data['警徽票标记'] * is_civilian

    data['平民警徽票正确标记'] = data['警徽票正确标记'] * is_civilian

    data = assign_first_check_markers(data)

    data = assign_mixed_blood_model_markers(data)

    data = assign_dream_first_wolf_markers(data)

    data = assign_blind_poison_markers(data)

    data = assign_fake_gold_markers(data)

    data = assign_lagan_markers(data)

    data = assign_red_wolf_knife_markers(data)

    data = assign_first_knife_witch_markers(data)

    data['非首局标记'] = (~data['日期'].map(_is_first_session_game)).astype(int)

    data['非首局狼次数标记'] = (

        data['非首局标记']

        * (role.astype('string').str.strip() == PLAIN_WOLF_IDENTITY).astype(int)

    )

    return data



def build_player_stats(data, include_non_first_wolf_rate=False):

    """按姓名汇总并计算比率。"""

    tmp = data.assign(

        狼存活天数=data['存活天数'] * data['狼标记'],

        好人存活天数=data['存活天数'] * data['好人标记'],

    )

    agg_spec = dict(

        出场次数=('姓名', 'count'),

        胜场次数=('胜利标记', 'sum'),

        狼次数=('狼标记', 'sum'),

        技能狼次数=('技能狼标记', 'sum'),

        悍跳次数=('悍跳标记', 'sum'),

        拉杆次数=('拉杆标记', 'sum'),

        拉杆成功次数=('拉杆成功标记', 'sum'),

        起跳预言家次数=('起跳预言家标记', 'sum'),

        自爆次数=('自爆标记', 'sum'),

        非盗宝红狼次数=('非盗宝红狼标记', 'sum'),

        自刀次数=('自刀标记', 'sum'),

        狼队友自刀次数=('狼队友自刀标记', 'sum'),

        首刀女巫次数=('首刀女巫标记', 'sum'),

        好人次数=('好人标记', 'sum'),

        好人胜利次数=('好人胜利标记', 'sum'),

        女巫毒师次数=('女巫毒师标记', 'sum'),

        压毒次数=('压毒标记', 'sum'),

        毒药使用次数=('毒药使用标记', 'sum'),

        毒狼次数=('毒狼人标记', 'sum'),

        猎人次数=('猎人标记', 'sum'),

        猎人技能次数=('猎人技能次数', 'sum'),

        猎人技能狼人次数=('猎人技能狼人次数', 'sum'),

        盲毒次数=('盲毒标记', 'sum'),

        盲毒狼人次数=('盲毒狼人标记', 'sum'),

        摄梦人次数=('摄梦人标记', 'sum'),

        首摄狼人次数=('首摄狼人标记', 'sum'),

        首摄狼王盗宝猎人次数=('首摄狼王盗宝猎人标记', 'sum'),

        被盲毒次数=('被盲毒标记', 'sum'),

        非狼被盲毒次数=('非狼被盲毒标记', 'sum'),

        被首验次数=('被首验标记', 'sum'),

        混血儿榜样次数=('混血儿榜样标记', 'sum'),

        接狼人金水次数=('假金标记', 'sum'),

        机械狼次数=('机械狼标记', 'sum'),

        机械女巫次数=('机械女巫标记', 'sum'),

        机械猎人次数=('机械猎人标记', 'sum'),

        机械守卫次数=('机械守卫标记', 'sum'),

        机械通灵师次数=('机械通灵师标记', 'sum'),

        机械双刀次数=('机械双刀标记', 'sum'),

        机械平民次数=('机械平民标记', 'sum'),

        警徽票正确次数=('警徽票正确标记', 'sum'),

        警徽票次数=('警徽票标记', 'sum'),

        平民放逐票次数=('平民放逐票', 'sum'),

        平民正确放逐票次数=('平民正确放逐票', 'sum'),

        平民警徽票次数=('平民警徽票标记', 'sum'),

        平民警徽票正确次数=('平民警徽票正确标记', 'sum'),

        好人警下次数=('警下标记', 'sum'),

        身份次数=('身份标记', 'sum'),

        预通次数=('预通标记', 'sum'),

        预通被放逐次数=('预通被放逐标记', 'sum'),

        预通被毒次数=('预通被毒标记', 'sum'),

        预通被枪次数=('预通被枪标记', 'sum'),

        预通获警徽次数=('预通获警徽标记', 'sum'),

        预通被奶死次数=('预通被奶死标记', 'sum'),

        预通被盲毒次数=('预通被盲毒标记', 'sum'),

        预通被代跳次数=('预通被代跳标记', 'sum'),

        神职身份次数=('神职身份标记', 'sum'),

        狼胜利次数=('狼胜利标记', 'sum'),

        正确放逐票次数=('正确放逐票', 'sum'),

        放逐票次数=('放逐票次数', 'sum'),

        无预通生推正确放逐票次数=('无预通生推正确放逐票', 'sum'),

        无预通放逐票次数=('无预通放逐票', 'sum'),

        存活天数总和=('存活天数', 'sum'),

        狼存活天数总和=('狼存活天数', 'sum'),

        好人存活天数总和=('好人存活天数', 'sum'),

    )

    if include_non_first_wolf_rate:

        agg_spec['非首局出场次数'] = ('非首局标记', 'sum')

        agg_spec['非首局狼次数'] = ('非首局狼次数标记', 'sum')

    stat = tmp.groupby('姓名').agg(**agg_spec).reset_index()

    stat = stat.rename(columns={'首摄狼王盗宝猎人次数': '首摄狼王/盗宝猎人次数'})

    stat = stat.merge(summarize_player_game_lists(data), on='姓名', how='left')

    stat['参与场次'] = stat['参与场次'].fillna('')

    stat['胜利场次'] = stat['胜利场次'].fillna('')

    stat = stat.merge(summarize_seat_number_counts(data), on='姓名', how='left')

    stat['座位号次数'] = stat['座位号次数'].fillna('')

    stat = stat.merge(summarize_prophet_first_check_players(data), on='姓名', how='left')

    stat['首验'] = stat['首验'].fillna('')

    stat = stat.merge(summarize_first_checked_by(data), on='姓名', how='left')

    stat['被首验'] = stat['被首验'].fillna('')

    stat = stat.merge(summarize_blind_poison_wolves(data), on='姓名', how='left')

    stat['盲毒狼人'] = stat['盲毒狼人'].fillna('')

    stat = stat.merge(summarize_poison_records(data), on='姓名', how='left')

    stat['毒药记录'] = stat['毒药记录'].fillna('')

    stat = stat.merge(summarize_hunter_skill_records(data), on='姓名', how='left')

    stat['猎人技能记录'] = stat['猎人技能记录'].fillna('')

    stat = stat.merge(summarize_mixed_blood_records(data), on='姓名', how='left')

    stat['混血儿记录'] = stat['混血儿记录'].fillna('')

    stat = stat.merge(summarize_fake_gold_givers(data), on='姓名', how='left')

    stat['接狼人金水'] = stat['接狼人金水'].fillna('')

    stat = stat.merge(summarize_lagan_records(data), on='姓名', how='left')

    stat['拉杆记录'] = stat['拉杆记录'].fillna('')

    stat = stat.merge(summarize_sheriff_vote_error_records(data), on='姓名', how='left')

    stat['警上站狼边'] = stat['警上站狼边'].fillna('')

    stat = stat.merge(summarize_prophet_didi_records(data), on='姓名', how='left')

    stat['预通滴滴记录'] = stat['预通滴滴记录'].fillna('')

    stat = stat.merge(summarize_identity_win_rates(data), on='姓名', how='left')

    stat['身份胜率'] = stat['身份胜率'].fillna('')

    stat = stat.merge(summarize_banxing_win_rates(data), on='姓名', how='left')

    stat['版型胜率'] = stat['版型胜率'].fillna('')

    stat = stat.merge(summarize_banxing_wolf_rates(data), on='姓名', how='left')

    stat['版型狼人率'] = stat['版型狼人率'].fillna('')

    stat['平均存活天数'] = (stat['存活天数总和'] / stat['出场次数']).round(1)

    stat['狼人平均存活天数'] = (

        stat['狼存活天数总和'] / stat['狼次数'].replace(0, pd.NA)

    ).fillna(0).round(1)

    stat['好人平均存活天数'] = (

        stat['好人存活天数总和'] / stat['好人次数'].replace(0, pd.NA)

    ).fillna(0).round(1)

    stat = stat.drop(columns=['存活天数总和', '狼存活天数总和', '好人存活天数总和'])

    rate_cols = get_rate_cols(include_non_first_wolf_rate)

    for name, (num, den) in rate_cols.items():

        stat[name] = (stat[num] / stat[den].replace(0, pd.NA)).fillna(0)

    stat = stat.sort_values('出场次数', ascending=False).reset_index(drop=True)

    stat[list(rate_cols)] = stat[list(rate_cols)].map(lambda x: f'{x:.1%}')

    return stat



def build_banxing_stats(data):

    """按版型汇总对局数据。"""

    rows = []

    for (date, banxing), group in data.groupby(['日期', '版型']):

        win = group['胜利'].dropna().iloc[0] if group['胜利'].notna().any() else None

        duration = game_duration(group)

        for bx in split_banxing(banxing, group):

            rows.append({'日期': date, '版型': bx, '胜利': win, '持续天数': duration})

    games = pd.DataFrame(rows)

    games['结果'] = games['胜利'].map({'狼': '狼赢', '好人': '好人赢'}).fillna('')

    banxing = games.groupby('版型', as_index=False).agg(

        总场次=('结果', 'count'),

        狼赢次数=('结果', lambda s: (s == '狼赢').sum()),

        平均持续天数=('持续天数', 'mean'),

    )

    banxing['平均持续天数'] = banxing['平均持续天数'].round(1)

    yvlhb = banxing[banxing['版型'].isin(YVLHB_CHILDREN)]

    if not yvlhb.empty:

        total = yvlhb['总场次'].sum()

        wolf_wins = yvlhb['狼赢次数'].sum()

        avg_days = (

            (yvlhb['总场次'] * yvlhb['平均持续天数']).sum() / total

            if total else 0.0

        )

        banxing = banxing[~banxing['版型'].eq('预女猎白混')]

        banxing = pd.concat([

            banxing,

            pd.DataFrame([{

                '版型': '预女猎白混',

                '总场次': total,

                '狼赢次数': wolf_wins,

                '平均持续天数': round(avg_days, 1),

            }]),

        ], ignore_index=True)

    daobao = banxing[banxing['版型'].isin(DAOBAO_ROLES)]

    if not daobao.empty:

        total = daobao['总场次'].sum()

        wolf_wins = daobao['狼赢次数'].sum()

        avg_days = (

            (daobao['总场次'] * daobao['平均持续天数']).sum() / total

            if total else 0.0

        )

        banxing = banxing[~banxing['版型'].eq('盗宝大师')]

        banxing = pd.concat([

            banxing,

            pd.DataFrame([{

                '版型': '盗宝大师',

                '总场次': total,

                '狼赢次数': wolf_wins,

                '平均持续天数': round(avg_days, 1),

            }]),

        ], ignore_index=True)

    missing_roles = (

        [r for r in DAOBAO_ROLES if r not in banxing['版型'].values]

        + [r for r in JIXIE_ROLES if r not in banxing['版型'].values]

        + [r for r in ['预女猎白混', '盗宝大师'] + YVLHB_CHILDREN if r not in banxing['版型'].values]

    )

    if missing_roles:

        banxing = pd.concat([

            banxing,

            pd.DataFrame({'版型': missing_roles, '总场次': 0, '狼赢次数': 0, '平均持续天数': 0.0}),

        ], ignore_index=True)

    banxing['好人赢次数'] = banxing['总场次'] - banxing['狼赢次数']

    banxing['狼人胜率'] = (banxing['狼赢次数'] / banxing['总场次'].replace(0, pd.NA)).fillna(0)

    banxing = banxing.sort_values('总场次', ascending=False).reset_index(drop=True)

    banxing['狼人胜率'] = banxing['狼人胜率'].map(lambda x: f'{x:.1%}')

    return banxing



def merge_banxing_stats(frames):

    """合并多赛季版型统计数据。"""

    columns = ['版型', '总场次', '狼赢次数', '好人赢次数', '平均持续天数', '狼人胜率']

    if not frames:

        return pd.DataFrame(columns=columns)

    combined = pd.concat(frames, ignore_index=True)

    combined['_持续天数加权'] = combined['总场次'] * combined['平均持续天数']

    merged = combined.groupby('版型', as_index=False).agg(

        总场次=('总场次', 'sum'),

        狼赢次数=('狼赢次数', 'sum'),

        _持续天数加权=('_持续天数加权', 'sum'),

    )

    merged['平均持续天数'] = (

        merged['_持续天数加权'] / merged['总场次'].replace(0, pd.NA)

    ).fillna(0).round(1)

    merged['好人赢次数'] = merged['总场次'] - merged['狼赢次数']

    merged['狼人胜率'] = (

        merged['狼赢次数'] / merged['总场次'].replace(0, pd.NA)

    ).fillna(0)

    merged = merged.drop(columns=['_持续天数加权'])

    merged = merged.sort_values('总场次', ascending=False).reset_index(drop=True)

    merged['狼人胜率'] = merged['狼人胜率'].map(lambda x: f'{x:.1%}')

    return merged[columns]



def build_tongbian_stats(data, stat_df, min_appearances=6):

    """按对局（日期+版型）统计选手对的同边率与同边胜率（胜场按阵营判定）；仅含出场次数>=min_appearances 的选手。"""

    from itertools import combinations

    eligible = set(stat_df.loc[stat_df['出场次数'] >= min_appearances, '姓名'])

    pair_acc = {}

    def pair_key(a, b):

        a, b = str(a), str(b)

        return (a, b) if a <= b else (b, a)

    wolf_camps = {'狼人', '狼人混'}

    def is_wolf_camp(camp):

        return camp in wolf_camps

    def format_tongbian_session(date_val, name_a, identity_a, name_b, identity_b, win):

        if pd.isna(date_val):

            date_str = ''

        else:

            date_str = str(int(date_val))

        win_str = '—' if win is None or (isinstance(win, float) and pd.isna(win)) else str(win).strip()

        id_a = '—' if pd.isna(identity_a) else str(identity_a).strip()

        id_b = '—' if pd.isna(identity_b) else str(identity_b).strip()

        return f'{date_str}（{name_a}：{id_a}、{name_b}：{id_b}、胜利方：{win_str}）'

    def empty_counts():

        return {

            '同场次数': 0, '同边次数': 0, '同狼人次数': 0, '同好人次数': 0,

            '同边狼人次数': 0, '同边狼人胜次数': 0, '同边好人胜次数': 0,

            '同边场次': [],

        }

    for (date_val, _), group in data.groupby(['日期', '版型']):

        players = group[['姓名', '阵营', '身份']].drop_duplicates('姓名')

        players = players[players['姓名'].isin(eligible)]

        if len(players) < 2:

            continue

        win = group['胜利'].dropna().iloc[0] if group['胜利'].notna().any() else None

        rec = players.set_index('姓名')

        for a, b in combinations(rec.index, 2):

            k = pair_key(a, b)

            if k not in pair_acc:

                pair_acc[k] = empty_counts()

            acc = pair_acc[k]

            acc['同场次数'] += 1

            ca, cb = rec.loc[a, '阵营'], rec.loc[b, '阵营']

            both_wolf = is_wolf_camp(ca) and is_wolf_camp(cb)

            both_good = not is_wolf_camp(ca) and not is_wolf_camp(cb)

            if both_wolf:

                acc['同狼人次数'] += 1

            if both_good:

                acc['同好人次数'] += 1

            if not (is_wolf_camp(ca) == is_wolf_camp(cb)):

                continue

            acc['同边次数'] += 1

            acc['同边场次'].append(

                format_tongbian_session(

                    date_val, a, rec.loc[a, '身份'], b, rec.loc[b, '身份'], win

                )

            )

            if both_wolf:

                acc['同边狼人次数'] += 1

                if win == '狼':

                    acc['同边狼人胜次数'] += 1

            if both_good and win == '好人':

                acc['同边好人胜次数'] += 1

    rows = []

    for (a, b), acc in pair_acc.items():

        co = acc['同场次数']

        same = acc['同边次数']

        same_wolf = acc['同边狼人次数']

        rows.append({

            '姓名A': a,

            '姓名B': b,

            '同场次数': co,

            '同边次数': same,

            '同边狼人次数': same_wolf,

            '同边率': (same / co) if co else 0,

            '同边狼人胜率': (acc['同边狼人胜次数'] / same_wolf) if same_wolf else 0,

            '同边好人胜率': (acc['同边好人胜次数'] / acc['同好人次数']) if acc['同好人次数'] else 0,

            '同边场次': ','.join(acc['同边场次']),

        })

    if not rows:

        return pd.DataFrame(columns=[

            '姓名A', '姓名B', '同场次数', '同边次数', '同边狼人次数',

            '同边率', '同边狼人胜率', '同边好人胜率', '同边场次',

        ])

    out = pd.DataFrame(rows)

    for col in ('同边率', '同边狼人胜率', '同边好人胜率'):

        out[col] = out[col].map(lambda x: f'{x:.1%}')

    return out.sort_values(['同场次数', '姓名A', '姓名B'], ascending=[False, True, True]).reset_index(drop=True)



def export_sheet(excel_file, prefix, sheet):

    """读取单个表单并输出 JSON / Excel 到 data 目录，文件名以 prefix+sheet 为前缀。"""

    os.makedirs(DATA_DIR, exist_ok=True)

    tag = f'{prefix}{sheet}'

    def out_path(name):

        return os.path.join(DATA_DIR, f'{tag}{name}')

    df = pd.read_excel(excel_file, sheet_name=sheet)

    df = normalize_special_exile_column(df)

    df = normalize_d1_check_result_column(df)

    df = assign_camp_from_identity(df)

    run_data_checks(df, tag=tag)

    prepare_raw_export_df(df).to_json(

        out_path('原始数据.json'), force_ascii=False, orient='records'

    )

    df = merge_vote_camps(df)

    df = add_markers(df)

    stat_df = build_player_stats(

        df,

        include_non_first_wolf_rate=(prefix == NON_FIRST_WOLF_DATASET_PREFIX),

    )

    banxing_df = build_banxing_stats(df)

    tongbian_df = build_tongbian_stats(df, stat_df)

    stat_df.to_json(out_path('玩家统计.json'), orient='records', force_ascii=False, indent=4)

    banxing_df.to_json(out_path('版型数据.json'), orient='records', force_ascii=False, indent=4)

    tongbian_df.to_json(out_path('同边数据.json'), orient='records', force_ascii=False, indent=4)

    for path, frame in (

        (out_path('玩家统计.xlsx'), stat_df),

        (out_path('版型数据.xlsx'), banxing_df),

        (out_path('同边数据.xlsx'), tongbian_df),

    ):

        if os.path.exists(path):

            os.remove(path)

        frame.to_excel(path, index=False)

    return stat_df, banxing_df, tongbian_df, df



# ---------- 主流程 ----------



export_statistics_rules()



sheet_results = {}



for excel_file, prefix, sheets in DATASETS:

    season_banxing_frames = []

    marked_frames = []

    for sheet in sheets:

        stat_df, banxing_df, tongbian_df, marked_df = export_sheet(excel_file, prefix, sheet)

        sheet_results[f'{prefix}{sheet}'] = (stat_df, banxing_df, tongbian_df)

        season_banxing_frames.append(banxing_df)

        marked_frames.append(marked_df)

    seat_number_df = build_seat_number_stats(pd.concat(marked_frames, ignore_index=True))

    seat_number_tag = f'{prefix}座位号数据统计'

    seat_number_xlsx = os.path.join(DATA_DIR, f'{seat_number_tag}.xlsx')

    seat_number_json = os.path.join(DATA_DIR, f'{seat_number_tag}.json')

    if os.path.exists(seat_number_xlsx):

        try:

            os.remove(seat_number_xlsx)

        except OSError:

            pass

    seat_number_df.to_excel(seat_number_xlsx, index=False)

    seat_number_df.to_json(seat_number_json, orient='records', force_ascii=False, indent=4)

    total_banxing_df = merge_banxing_stats(season_banxing_frames)

    total_tag = f'{prefix}总'

    total_banxing_df.to_json(

        os.path.join(DATA_DIR, f'{total_tag}版型数据.json'),

        orient='records',

        force_ascii=False,

        indent=4,

    )

    total_banxing_xlsx = os.path.join(DATA_DIR, f'{total_tag}版型数据.xlsx')

    if os.path.exists(total_banxing_xlsx):

        os.remove(total_banxing_xlsx)

    total_banxing_df.to_excel(total_banxing_xlsx, index=False)

    sheet_results[f'{total_tag}'] = (None, total_banxing_df, None)



stat_df, banxing_df, tongbian_df = sheet_results['京城大师赛S22']



stat_df[stat_df['出场次数'] >= 3]



