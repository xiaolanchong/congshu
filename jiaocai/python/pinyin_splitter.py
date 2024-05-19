import dataclasses

@dataclasses.dataclass
class Syllable:
    syl: str
    tone: int

vowel_tones = {
    'a': 'āáǎà',
    'e': 'ēéěè',
    'ī': 'īíǐì',
    'o': 'ōóǒò',
    'u': 'ūúǔù',
    'ü': 'ǖǘǚǜ',
}


def get_all_syllables():
    syll_table = """
    a ba pa ma fa da ta na la ga ka ha zha cha sha za ca sa
    ai bai pai mai dai tai nai lai gai kai hai zhai chai shai zai cai sai
    an ban pan man fan dan tan nan lan gan kan han zhan chan shan ran zan can san
    ang bang pang mang fang dang tang nang lang gang kang hang zhang chang shang rang zang cang sang
    ao bao pao mao dao tao nao lao gao kao hao zhao chao shao rao zao cao sao
    e me de te ne le ge ke he zhe che she re ze ce se
    ei bei pei mei fei dei nei lei gei hei shei zei
    en ben pen men fen den nen gen ken hen zhen chen shen ren zen cen sen
    beng peng meng feng deng teng neng leng geng keng heng zheng cheng sheng reng zeng ceng seng
    er
    yi bi pi mi di ti ni li ji qi xi zhi chi shi ri zi ci si
    ya dia lia jia qia xia
    yan bian pian mian dian tian nian lian jian qian xian
    yang niang liang jiang qiang xiang
    yao biao piao miao diao tiao niao liao jiao qiao xiao
    ye bie pie mie die tie nie lie jie qie xie
    yin bin pin min nin lin jin qin xin
    ying bing ping ming ding ting ning ling jing qing xing
    yo
    yong jiong qiong xiong
    you miu diu niu liu jiu qiu xiu
    o bo po mo fo lo
    weng dong tong nong long gong kong hong zhong chong rong zong cong song
    ou pou mou fou dou tou nou lou gou kou hou zhou chou shou rou zou cou sou
    wu bu pu mu fu du tu nu lu gu ku hu zhu chu shu ru zu cu su
    wa gua kua hua zhua shua
    wai guai kuai huai chuai shuai
    wan duan tuan nuan luan guan kuan huan zhuan chuan shuan ruan zuan cuan suan
    wang guang kuang huang zhuang chuang shuang
    yue nüe lüe jue que xue
    wei dui tui gui kui hui zhui chui shui rui zui cui sui
    wen dun tun lun gun kun hun zhun chun shun run zun cun sun
    wo duo tuo nuo luo guo kuo huo zhuo chuo shuo ruo zuo cuo suo
    yu nü lü ju qu xu
    yuan juan quan xuan
    yun jun qun xun
    """
    all_syllables = []

    def add_letter_syllables(syl:str, letter:str):
        idx = syl.find(letter)
        if idx != -1:
            for tone in vowel_tones[letter]:
                all_syllables.append(syl[:idx] + tone + syl[idx + 1:])
            all_syllables.append(syl)
            return True
        return False
    for line in syll_table.split('\n'):
        line = line.strip()
        if line == '':
            continue
        for syl in line.split(' '):
            if add_letter_syllables(syl, 'a') or add_letter_syllables(syl, 'e'):
                continue
            o_idx = syl.find('o')
            u_idx = syl.find('u')
            if o_idx != -1 and u_idx != -1 and o_idx < u_idx:  # ou
                add_letter_syllables(syl, 'o')
                continue
            for idx, letter in enumerate(syl[::-1]):
                if letter in vowel_tones.keys():
                    add_letter_syllables(syl, letter)
    return all_syllables


class PinyinSplitter:
    def __init__(self):
        self.all_syllables = set(get_all_syllables())
        print(self.all_syllables)

    def split(self, pinyin: str) -> list[Syllable]:
        alternatives = []
        def split_recursively(pos, before:list[str]):
            


a = PinyinSplitter()
