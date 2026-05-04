import csv
import json
import os
import re
from datetime import date


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POS_LABELS_KO = {
    "Nouns": "명사",
    "Adjectives": "형용사",
    "Verbs": "동사",
    "Adverbs": "부사",
}

DETAILS = {
    "achievement": {"meaning_ko": "업적, 성취", "example_en": "Winning the award was a major achievement.", "example_ko": "그 상을 받은 것은 큰 성취였다.", "synonyms": ["accomplishment"], "antonyms": ["failure"]},
    "award": {"meaning_ko": "상, 수상", "example_en": "She received an award for her project.", "example_ko": "그녀는 프로젝트로 상을 받았다.", "synonyms": ["prize"], "antonyms": []},
    "(summer) camp": {"meaning_ko": "여름 캠프", "example_en": "I made new friends at summer camp.", "example_ko": "나는 여름 캠프에서 새 친구들을 사귀었다.", "synonyms": ["camp program"], "antonyms": []},
    "(body) cast": {"meaning_ko": "몸에 하는 깁스", "example_en": "He wore a body cast after the accident.", "example_ko": "그는 사고 후 몸에 깁스를 했다.", "synonyms": ["plaster cast"], "antonyms": []},
    "chess": {"meaning_ko": "체스", "example_en": "Chess helps me think ahead.", "example_ko": "체스는 내가 앞을 내다보며 생각하는 데 도움이 된다.", "synonyms": ["board game"], "antonyms": []},
    "childhood": {"meaning_ko": "어린 시절", "example_en": "This song reminds me of my childhood.", "example_ko": "이 노래는 내 어린 시절을 떠올리게 한다.", "synonyms": ["early years"], "antonyms": ["adulthood"]},
    "comic book": {"meaning_ko": "만화책", "example_en": "He collects old comic books.", "example_ko": "그는 오래된 만화책을 모은다.", "synonyms": ["graphic novel"], "antonyms": []},
    "contact information": {"meaning_ko": "연락처 정보", "example_en": "Please write your contact information here.", "example_ko": "여기에 연락처 정보를 적어 주세요.", "synonyms": ["contact details"], "antonyms": []},
    "courage": {"meaning_ko": "용기", "example_en": "It took courage to speak honestly.", "example_ko": "솔직하게 말하는 데는 용기가 필요했다.", "synonyms": ["bravery"], "antonyms": ["fear"]},
    "headline": {"meaning_ko": "헤드라인, 기사 제목", "example_en": "The headline caught my attention.", "example_ko": "그 헤드라인이 내 관심을 끌었다.", "synonyms": ["title"], "antonyms": []},
    "hide-and-seek": {"meaning_ko": "숨바꼭질", "example_en": "The children played hide-and-seek outside.", "example_ko": "아이들은 밖에서 숨바꼭질을 했다.", "synonyms": ["children's game"], "antonyms": []},
    "hobby": {"meaning_ko": "취미", "example_en": "Photography is my favorite hobby.", "example_ko": "사진 촬영은 내가 가장 좋아하는 취미다.", "synonyms": ["pastime"], "antonyms": []},
    "hometown": {"meaning_ko": "고향", "example_en": "I visit my hometown every summer.", "example_ko": "나는 매년 여름 고향을 방문한다.", "synonyms": ["birthplace"], "antonyms": []},
    "illness": {"meaning_ko": "질병, 병", "example_en": "She missed school because of an illness.", "example_ko": "그녀는 병 때문에 학교에 빠졌다.", "synonyms": ["sickness"], "antonyms": ["health"]},
    "immigrant": {"meaning_ko": "이민자", "example_en": "His grandparents were immigrants.", "example_ko": "그의 조부모님은 이민자였다.", "synonyms": ["newcomer"], "antonyms": []},
    "interest": {"meaning_ko": "관심, 흥미", "example_en": "She has an interest in politics.", "example_ko": "그녀는 정치에 관심이 있다.", "synonyms": ["curiosity"], "antonyms": ["disinterest"]},
    "memory": {"meaning_ko": "기억, 추억", "example_en": "That trip is a happy memory.", "example_ko": "그 여행은 행복한 추억이다.", "synonyms": ["recollection"], "antonyms": []},
    "outdoors": {"meaning_ko": "야외, 집 밖", "example_en": "We spent the whole day outdoors.", "example_ko": "우리는 하루 종일 야외에서 시간을 보냈다.", "synonyms": ["outside"], "antonyms": ["indoors"]},
    "pet": {"meaning_ko": "반려동물", "example_en": "My first pet was a small dog.", "example_ko": "내 첫 반려동물은 작은 개였다.", "synonyms": ["animal companion"], "antonyms": []},
    "playground": {"meaning_ko": "놀이터", "example_en": "The kids ran to the playground.", "example_ko": "아이들은 놀이터로 달려갔다.", "synonyms": ["play area"], "antonyms": []},
    "politics": {"meaning_ko": "정치", "example_en": "They often discuss politics at dinner.", "example_ko": "그들은 저녁 식사 때 정치 이야기를 자주 한다.", "synonyms": ["government affairs"], "antonyms": []},
    "possession": {"meaning_ko": "소유물, 소유", "example_en": "This necklace is my most valuable possession.", "example_ko": "이 목걸이는 내 가장 소중한 소유물이다.", "synonyms": ["belonging"], "antonyms": []},
    "profile": {"meaning_ko": "프로필, 인물 소개", "example_en": "Update your profile with a new photo.", "example_ko": "새 사진으로 프로필을 업데이트하세요.", "synonyms": ["personal page"], "antonyms": []},
    "recreation": {"meaning_ko": "여가 활동, 오락", "example_en": "The park offers many forms of recreation.", "example_ko": "그 공원은 여러 가지 여가 활동을 제공한다.", "synonyms": ["leisure"], "antonyms": ["work"]},
    "relatives": {"meaning_ko": "친척들", "example_en": "We invited all our relatives to dinner.", "example_ko": "우리는 모든 친척을 저녁 식사에 초대했다.", "synonyms": ["family members"], "antonyms": []},
    "role": {"meaning_ko": "역할", "example_en": "Everyone has a role in the group.", "example_ko": "모든 사람은 그 모임에서 역할이 있다.", "synonyms": ["part"], "antonyms": []},
    "scary movies": {"meaning_ko": "무서운 영화, 공포 영화", "example_en": "I do not like watching scary movies alone.", "example_ko": "나는 공포 영화를 혼자 보는 것을 좋아하지 않는다.", "synonyms": ["horror movies"], "antonyms": []},
    "self-portrait": {"meaning_ko": "자화상", "example_en": "The artist painted a self-portrait.", "example_ko": "그 화가는 자화상을 그렸다.", "synonyms": ["portrait of oneself"], "antonyms": []},
    "social networking": {"meaning_ko": "소셜 네트워킹, SNS 활동", "example_en": "Social networking helps people stay connected.", "example_ko": "소셜 네트워킹은 사람들이 계속 연결되도록 돕는다.", "synonyms": ["social media use"], "antonyms": []},
    "specialist": {"meaning_ko": "전문가, 전문의", "example_en": "The doctor sent me to a specialist.", "example_ko": "의사는 나를 전문의에게 보냈다.", "synonyms": ["expert"], "antonyms": ["generalist"]},
    "stickers": {"meaning_ko": "스티커들", "example_en": "She put stickers on her notebook.", "example_ko": "그녀는 공책에 스티커를 붙였다.", "synonyms": ["labels"], "antonyms": []},
    "superhero": {"meaning_ko": "슈퍼히어로", "example_en": "The movie is about a young superhero.", "example_ko": "그 영화는 어린 슈퍼히어로에 관한 이야기다.", "synonyms": ["hero"], "antonyms": ["villain"]},
    "taste": {"meaning_ko": "맛, 취향", "example_en": "We have different tastes in music.", "example_ko": "우리는 음악 취향이 다르다.", "synonyms": ["preference"], "antonyms": []},
    "teddy bear": {"meaning_ko": "곰 인형", "example_en": "The child slept with a teddy bear.", "example_ko": "그 아이는 곰 인형을 안고 잤다.", "synonyms": ["stuffed bear"], "antonyms": []},
    "thriller": {"meaning_ko": "스릴러", "example_en": "This thriller has a surprising ending.", "example_ko": "이 스릴러는 놀라운 결말이 있다.", "synonyms": ["suspense story"], "antonyms": []},
    "toy car": {"meaning_ko": "장난감 자동차", "example_en": "He played with a toy car on the floor.", "example_ko": "그는 바닥에서 장난감 자동차를 가지고 놀았다.", "synonyms": ["model car"], "antonyms": []},
    "video game": {"meaning_ko": "비디오 게임", "example_en": "This video game is popular online.", "example_ko": "이 비디오 게임은 온라인에서 인기가 있다.", "synonyms": ["computer game"], "antonyms": []},
    "basic": {"meaning_ko": "기본적인", "example_en": "The course teaches basic grammar.", "example_ko": "그 강좌는 기본 문법을 가르친다.", "synonyms": ["fundamental"], "antonyms": ["advanced"]},
    "current": {"meaning_ko": "현재의, 최신의", "example_en": "What is your current address?", "example_ko": "현재 주소가 어떻게 되나요?", "synonyms": ["present"], "antonyms": ["past"]},
    "far": {"meaning_ko": "먼", "example_en": "The station is far from here.", "example_ko": "역은 여기서 멀다.", "synonyms": ["distant"], "antonyms": ["near"]},
    "fit": {"meaning_ko": "건강한, 알맞은", "example_en": "Regular exercise keeps you fit.", "example_ko": "규칙적인 운동은 건강을 유지하게 해 준다.", "synonyms": ["healthy"], "antonyms": ["unfit"]},
    "good (at)": {"meaning_ko": "~을 잘하는", "example_en": "She is good at chess.", "example_ko": "그녀는 체스를 잘한다.", "synonyms": ["skilled at"], "antonyms": ["bad at"]},
    "messy": {"meaning_ko": "지저분한, 엉망인", "example_en": "My room is messy after the weekend.", "example_ko": "주말이 지나고 내 방은 지저분하다.", "synonyms": ["untidy"], "antonyms": ["neat"]},
    "neat": {"meaning_ko": "깔끔한", "example_en": "His desk is always neat.", "example_ko": "그의 책상은 항상 깔끔하다.", "synonyms": ["tidy"], "antonyms": ["messy"]},
    "online": {"meaning_ko": "온라인의", "example_en": "I found the article online.", "example_ko": "나는 그 기사를 온라인에서 찾았다.", "synonyms": ["internet-based"], "antonyms": ["offline"]},
    "outdoor": {"meaning_ko": "야외의", "example_en": "We planned an outdoor activity.", "example_ko": "우리는 야외 활동을 계획했다.", "synonyms": ["outside"], "antonyms": ["indoor"]},
    "argue": {"meaning_ko": "논쟁하다, 다투다", "example_en": "They argue about politics sometimes.", "example_ko": "그들은 가끔 정치 문제로 논쟁한다.", "synonyms": ["debate"], "antonyms": ["agree"]},
    "collect": {"meaning_ko": "모으다, 수집하다", "example_en": "He likes to collect stickers.", "example_ko": "그는 스티커 모으는 것을 좋아한다.", "synonyms": ["gather"], "antonyms": []},
    "direct (a movie)": {"meaning_ko": "영화를 감독하다", "example_en": "She wants to direct a movie one day.", "example_ko": "그녀는 언젠가 영화를 감독하고 싶어 한다.", "synonyms": ["make a film"], "antonyms": []},
    "donate": {"meaning_ko": "기부하다", "example_en": "They donate money to the hospital.", "example_ko": "그들은 병원에 돈을 기부한다.", "synonyms": ["give"], "antonyms": []},
    "follow": {"meaning_ko": "따라가다, 팔로우하다", "example_en": "I follow her profile online.", "example_ko": "나는 온라인에서 그녀의 프로필을 팔로우한다.", "synonyms": ["track"], "antonyms": ["unfollow"]},
    "get (in trouble)": {"meaning_ko": "곤란해지다, 혼나다", "example_en": "You may get in trouble for being late.", "example_ko": "늦으면 혼날 수 있다.", "synonyms": ["be punished"], "antonyms": []},
    "keep fit": {"meaning_ko": "건강을 유지하다", "example_en": "I skate regularly to keep fit.", "example_ko": "나는 건강을 유지하려고 규칙적으로 스케이트를 탄다.", "synonyms": ["stay healthy"], "antonyms": []},
    "produce (a movie)": {"meaning_ko": "영화를 제작하다", "example_en": "The company will produce a movie this year.", "example_ko": "그 회사는 올해 영화를 제작할 것이다.", "synonyms": ["create a film"], "antonyms": []},
    "refer": {"meaning_ko": "언급하다, 지칭하다", "example_en": "This word can refer to a hobby or an interest.", "example_ko": "이 단어는 취미나 관심사를 지칭할 수 있다.", "synonyms": ["mention"], "antonyms": []},
    "remember": {"meaning_ko": "기억하다", "example_en": "I remember my childhood clearly.", "example_ko": "나는 어린 시절을 또렷이 기억한다.", "synonyms": ["recall"], "antonyms": ["forget"]},
    "skate": {"meaning_ko": "스케이트를 타다", "example_en": "We skate at the park afterwards.", "example_ko": "우리는 그 후에 공원에서 스케이트를 탄다.", "synonyms": ["roller-skate"], "antonyms": []},
    "take up": {"meaning_ko": "시작하다, 차지하다", "example_en": "I want to take up chess this year.", "example_ko": "나는 올해 체스를 시작하고 싶다.", "synonyms": ["start"], "antonyms": ["give up"]},
    "notice": {"meaning_ko": "알아차리다, 주목하다", "example_en": "Did you notice the headline?", "example_ko": "그 헤드라인을 알아차렸니?", "synonyms": ["observe"], "antonyms": ["miss"]},
    "urge": {"meaning_ko": "강력히 권하다, 촉구하다", "example_en": "Parents urge children to play outdoors.", "example_ko": "부모들은 아이들에게 야외에서 놀라고 권한다.", "synonyms": ["encourage"], "antonyms": []},
    "worry (about something)": {"meaning_ko": "~에 대해 걱정하다", "example_en": "Do not worry about the award results.", "example_ko": "수상 결과를 걱정하지 마라.", "synonyms": ["be anxious about"], "antonyms": []},
    "afterwards": {"meaning_ko": "그 후에, 나중에", "example_en": "We had lunch and went skating afterwards.", "example_ko": "우리는 점심을 먹고 그 후에 스케이트를 타러 갔다.", "synonyms": ["later"], "antonyms": ["beforehand"]},
    "regularly": {"meaning_ko": "규칙적으로, 정기적으로", "example_en": "She exercises regularly to keep fit.", "example_ko": "그녀는 건강을 유지하려고 규칙적으로 운동한다.", "synonyms": ["often"], "antonyms": ["rarely"]},
}

WORD_FORMS = {
    "achievement": {"verb": "achieve", "noun": "achievement", "adjective": "achievable"},
    "award": {"verb": "award", "noun": "award", "adjective": "award-winning"},
    "(summer) camp": {"verb": "camp", "noun": "camp", "adjective": "camping"},
    "(body) cast": {"verb": "cast", "noun": "cast"},
    "chess": {"noun": "chess"},
    "childhood": {"noun": "childhood", "adjective": "childhood"},
    "comic book": {"noun": "comic book", "adjective": "comic-book"},
    "contact information": {"verb": "contact", "noun": "contact information", "adjective": "contact"},
    "courage": {"verb": "encourage", "noun": "courage", "adjective": "courageous", "adverb": "courageously"},
    "headline": {"verb": "headline", "noun": "headline"},
    "hide-and-seek": {"noun": "hide-and-seek"},
    "hobby": {"noun": "hobby"},
    "hometown": {"noun": "hometown", "adjective": "hometown"},
    "illness": {"noun": "illness", "adjective": "ill"},
    "immigrant": {"verb": "immigrate", "noun": "immigrant / immigration", "adjective": "immigrant"},
    "interest": {"verb": "interest", "noun": "interest", "adjective": "interesting / interested", "adverb": "interestingly"},
    "memory": {"verb": "memorize / remember", "noun": "memory", "adjective": "memorable", "adverb": "memorably"},
    "outdoors": {"noun": "outdoors", "adjective": "outdoor", "adverb": "outdoors"},
    "pet": {"verb": "pet", "noun": "pet"},
    "playground": {"noun": "playground"},
    "politics": {"noun": "politics", "adjective": "political", "adverb": "politically"},
    "possession": {"verb": "possess", "noun": "possession", "adjective": "possessive"},
    "profile": {"verb": "profile", "noun": "profile"},
    "recreation": {"verb": "recreate", "noun": "recreation", "adjective": "recreational"},
    "relatives": {"verb": "relate", "noun": "relative / relatives", "adjective": "relative", "adverb": "relatively"},
    "role": {"noun": "role"},
    "scary movies": {"verb": "scare", "noun": "scary movie", "adjective": "scary"},
    "self-portrait": {"noun": "self-portrait"},
    "social networking": {"verb": "network", "noun": "social networking", "adjective": "social"},
    "specialist": {"verb": "specialize", "noun": "specialist", "adjective": "special", "adverb": "specially"},
    "stickers": {"verb": "stick", "noun": "sticker / stickers", "adjective": "sticky"},
    "superhero": {"noun": "superhero", "adjective": "superhero"},
    "taste": {"verb": "taste", "noun": "taste", "adjective": "tasty", "adverb": "tastefully"},
    "teddy bear": {"noun": "teddy bear"},
    "thriller": {"verb": "thrill", "noun": "thriller", "adjective": "thrilling"},
    "toy car": {"noun": "toy car"},
    "video game": {"noun": "video game", "adjective": "video-game"},
    "basic": {"noun": "basis / basics", "adjective": "basic", "adverb": "basically"},
    "current": {"noun": "current", "adjective": "current", "adverb": "currently"},
    "far": {"adjective": "far", "adverb": "far"},
    "fit": {"verb": "fit", "noun": "fitness", "adjective": "fit"},
    "good (at)": {"noun": "good", "adjective": "good at", "adverb": "well"},
    "messy": {"noun": "mess", "adjective": "messy", "adverb": "messily"},
    "neat": {"noun": "neatness", "adjective": "neat", "adverb": "neatly"},
    "online": {"adjective": "online", "adverb": "online"},
    "outdoor": {"noun": "outdoors", "adjective": "outdoor", "adverb": "outdoors"},
    "argue": {"verb": "argue", "noun": "argument", "adjective": "argumentative", "adverb": "argumentatively"},
    "collect": {"verb": "collect", "noun": "collection / collector", "adjective": "collective", "adverb": "collectively"},
    "direct (a movie)": {"verb": "direct", "noun": "director / direction", "adjective": "direct", "adverb": "directly"},
    "donate": {"verb": "donate", "noun": "donation / donor", "adjective": "donated"},
    "follow": {"verb": "follow", "noun": "follower", "adjective": "following"},
    "get (in trouble)": {"verb": "get in trouble", "noun": "trouble", "adjective": "troubled"},
    "keep fit": {"verb": "keep fit", "noun": "fitness", "adjective": "fit"},
    "produce (a movie)": {"verb": "produce", "noun": "producer / production", "adjective": "productive", "adverb": "productively"},
    "refer": {"verb": "refer", "noun": "reference", "adjective": "referential"},
    "remember": {"verb": "remember", "noun": "memory", "adjective": "memorable"},
    "skate": {"verb": "skate", "noun": "skate / skater / skating"},
    "take up": {"verb": "take up", "noun": "uptake"},
    "notice": {"verb": "notice", "noun": "notice", "adjective": "noticeable", "adverb": "noticeably"},
    "urge": {"verb": "urge", "noun": "urge", "adjective": "urgent", "adverb": "urgently"},
    "worry (about something)": {"verb": "worry about", "noun": "worry", "adjective": "worried", "adverb": "worriedly"},
    "afterwards": {"adverb": "afterwards"},
    "regularly": {"noun": "regularity", "adjective": "regular", "adverb": "regularly"},
}

SECOND_EXAMPLES = {
    "basic": {"en": "I only know the basic rules of chess.", "ko": "나는 체스의 기본 규칙만 알고 있다."},
    "current": {"en": "Her current hobby is collecting stickers.", "ko": "그녀의 현재 취미는 스티커를 모으는 것이다."},
    "far": {"en": "My hometown is far from this city.", "ko": "내 고향은 이 도시에서 멀다."},
    "fit": {"en": "He is fit because he exercises regularly.", "ko": "그는 규칙적으로 운동해서 건강하다."},
    "good (at)": {"en": "My cousin is good at video games.", "ko": "내 사촌은 비디오 게임을 잘한다."},
    "messy": {"en": "The playground was messy after the camp.", "ko": "캠프가 끝난 뒤 놀이터는 지저분했다."},
    "neat": {"en": "Please keep your profile page neat.", "ko": "프로필 페이지를 깔끔하게 유지해 주세요."},
    "online": {"en": "Online social networking can be useful.", "ko": "온라인 소셜 네트워킹은 유용할 수 있다."},
    "outdoor": {"en": "Outdoor recreation is popular in summer.", "ko": "야외 여가 활동은 여름에 인기가 많다."},
    "argue": {"en": "The relatives argue about politics every year.", "ko": "친척들은 매년 정치 문제로 논쟁한다."},
    "collect": {"en": "I collect comic books and toy cars.", "ko": "나는 만화책과 장난감 자동차를 모은다."},
    "direct (a movie)": {"en": "He hopes to direct a thriller someday.", "ko": "그는 언젠가 스릴러 영화를 감독하고 싶어 한다."},
    "donate": {"en": "The students donate toys after the camp.", "ko": "학생들은 캠프 후에 장난감을 기부한다."},
    "follow": {"en": "Many fans follow the superhero's profile online.", "ko": "많은 팬들이 그 슈퍼히어로의 프로필을 온라인에서 팔로우한다."},
    "get (in trouble)": {"en": "You can get in trouble if you hide contact information.", "ko": "연락처 정보를 숨기면 곤란해질 수 있다."},
    "keep fit": {"en": "Playing outdoors helps children keep fit.", "ko": "야외에서 노는 것은 아이들이 건강을 유지하는 데 도움이 된다."},
    "produce (a movie)": {"en": "The studio will produce a movie about his childhood.", "ko": "그 제작사는 그의 어린 시절에 관한 영화를 제작할 것이다."},
    "refer": {"en": "The headline can refer to an illness or an accident.", "ko": "그 헤드라인은 질병이나 사고를 지칭할 수 있다."},
    "remember": {"en": "I still remember my first teddy bear.", "ko": "나는 아직도 내 첫 곰 인형을 기억한다."},
    "skate": {"en": "We skate at the playground after school.", "ko": "우리는 방과 후 놀이터에서 스케이트를 탄다."},
    "take up": {"en": "She wants to take up chess this year.", "ko": "그녀는 올해 체스를 시작하고 싶어 한다."},
    "notice": {"en": "Did you notice the headline on the profile page?", "ko": "프로필 페이지의 헤드라인을 알아차렸니?"},
    "urge": {"en": "Doctors urge people to exercise outdoors.", "ko": "의사들은 사람들에게 야외에서 운동하라고 권한다."},
    "worry (about something)": {"en": "Parents often worry about their children's online profiles.", "ko": "부모들은 아이들의 온라인 프로필을 자주 걱정한다."},
    "afterwards": {"en": "We played hide-and-seek and had lunch afterwards.", "ko": "우리는 숨바꼭질을 하고 그 후에 점심을 먹었다."},
    "regularly": {"en": "She regularly updates her contact information.", "ko": "그녀는 연락처 정보를 정기적으로 업데이트한다."},
}


def parse_markdown(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    units = []
    current_unit = None
    current_section = None
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("# "):
            title = line[2:].strip()
            if current_unit is None:
                current_unit = {"title": "Unit 1", "subtitle": title, "sections": []}
                units.append(current_unit)
        elif line.startswith("## "):
            heading = line[3:].strip()
            if heading.lower().startswith("unit"):
                current_unit = {"title": heading, "subtitle": "", "sections": []}
                units.append(current_unit)
                current_section = None
            else:
                if current_unit is None:
                    current_unit = {"title": "Unit 1", "subtitle": "", "sections": []}
                    units.append(current_unit)
                current_section = {"title": heading, "words": []}
                current_unit["sections"].append(current_section)
        elif line.startswith("|") and current_section is not None:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            current_section["words"].extend(parse_table(table_lines, current_section["title"]))
            continue
        i += 1

    return units


def parse_table(lines: list[str], section_title: str) -> list[dict]:
    if len(lines) < 2:
        return []
    header = split_table_row(lines[0])
    rows = []
    for raw in lines[2:]:
        values = split_table_row(raw)
        if not values:
            continue
        row = dict(zip(header, values))
        word = row.get("Word", "").strip()
        if not word:
            continue
        detail = DETAILS.get(word, {})
        rows.append(
            {
                "word": word,
                "number": row.get("No.", row.get("No", "")).strip(),
                "part": section_title,
                "pos_ko": POS_LABELS_KO.get(section_title, section_title),
                "meaning_ko": pick(row, "Meaning", "Meaning Ko", "meaning_ko") or detail.get("meaning_ko", ""),
                "pronunciation": pick(row, "Pronunciation", "Pronunciation Ko", "pronunciation") or "",
                "word_forms": build_word_forms(word, section_title),
                "explanation": pick(row, "Explanation", "Explanation Ko", "explanation") or make_explanation(word, section_title),
                "examples": build_examples(row, detail, word, section_title),
                "synonyms": build_related_items(
                    pick(row, "Synonyms", "Similar", "synonyms") or detail.get("synonyms", []),
                    word,
                    "synonym",
                ),
                "antonyms": build_related_items(
                    pick(row, "Antonyms", "antonyms") or detail.get("antonyms", []),
                    word,
                    "antonym",
                ),
            }
        )
    return rows


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in next(csv.reader([line.strip().strip("|")], delimiter="|", skipinitialspace=True))]


def pick(row: dict, *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return value.strip()
    return ""


def list_values(value) -> list[str]:
    if isinstance(value, list):
        return value
    return [item.strip() for item in re.split(r"[,;/]", value) if item.strip()]


def build_related_items(value, base_word: str, relation: str) -> list[dict]:
    items = []
    for text in list_values(value):
        if isinstance(text, dict):
            items.append(text)
            continue
        items.append(
            {
                "en": text,
                "ko": make_related_meaning(text, base_word, relation),
                "example": make_related_example(text, base_word, relation),
            }
        )
    return items


def make_related_meaning(text: str, base_word: str, relation: str) -> str:
    if relation == "antonym":
        return f"'{base_word}'와 반대되는 뜻으로 함께 외우는 표현입니다."
    return f"'{base_word}'와 의미가 비슷한 표현입니다."


def make_related_example(text: str, base_word: str, relation: str) -> dict:
    clean = text.strip()
    if relation == "antonym":
        return {
            "en": f"The opposite idea is '{clean}'.",
            "ko": f"반대되는 개념은 '{clean}'입니다.",
        }
    return {
        "en": f"You can often use '{clean}' in a similar context.",
        "ko": f"비슷한 맥락에서 '{clean}'를 자주 쓸 수 있습니다.",
    }


def build_word_forms(word: str, section_title: str) -> dict:
    forms = dict(WORD_FORMS.get(word, {}))
    current_key = {
        "Nouns": "noun",
        "Adjectives": "adjective",
        "Verbs": "verb",
        "Adverbs": "adverb",
    }.get(section_title)
    if current_key and current_key not in forms:
        forms[current_key] = word.replace("(", "").replace(")", "")
    return forms


def build_examples(row: dict, detail: dict, word: str, section_title: str) -> list[dict]:
    first_en = pick(row, "Example EN", "Example", "example_en") or detail.get("example_en", "")
    first_ko = pick(row, "Example KO", "example_ko") or detail.get("example_ko", "")
    examples = []
    if first_en:
        examples.append({"en": first_en, "ko": first_ko})

    explicit_second_en = pick(row, "Example 2 EN", "Example2 EN", "example_2_en")
    explicit_second_ko = pick(row, "Example 2 KO", "Example2 KO", "example_2_ko")
    if explicit_second_en:
        examples.append({"en": explicit_second_en, "ko": explicit_second_ko})
    elif word in SECOND_EXAMPLES:
        examples.append(SECOND_EXAMPLES[word])
    else:
        examples.append(make_second_example(word, section_title))
    return examples[:2]


def make_second_example(word: str, section_title: str) -> dict:
    clean = word.replace("(", "").replace(")", "")
    if section_title == "Adjectives":
        return {
            "en": f"The situation felt {clean} to me.",
            "ko": f"그 상황은 나에게 {clean}한 느낌이었다.",
        }
    if section_title == "Verbs":
        return {
            "en": f"People often {clean} in everyday conversations.",
            "ko": f"사람들은 일상 대화에서 종종 {clean}라는 표현을 쓴다.",
        }
    if section_title == "Adverbs":
        return {
            "en": f"She checks her schedule {clean}.",
            "ko": f"그녀는 일정을 {clean} 확인한다.",
        }
    return {
        "en": f"We talked about {clean} in class.",
        "ko": f"우리는 수업에서 {clean}에 대해 이야기했다.",
    }


def make_explanation(word: str, section_title: str) -> str:
    return f"{POS_LABELS_KO.get(section_title, section_title)}로 쓰이는 기본 어휘입니다. 뜻과 예문을 함께 외우면 실제 문장에서 더 쉽게 떠올릴 수 있습니다."


def render_html(units: list[dict]) -> str:
    data = json.dumps(units, ensure_ascii=False).replace("</", "<\\/")
    generated = date.today().isoformat()
    total = sum(len(section["words"]) for unit in units for section in unit["sections"])
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Language Summary Vocabulary</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f5f7fb; color: #172033; }}
    header {{ background: #152238; color: #fff; padding: 24px 18px 18px; }}
    .wrap {{ max-width: 1120px; margin: 0 auto; }}
    h1 {{ margin: 0; font-size: 28px; letter-spacing: 0; }}
    .sub {{ margin: 8px 0 0; color: #c9d6e8; font-size: 14px; }}
    .toolbar {{ position: sticky; top: 0; z-index: 2; background: rgba(245,247,251,.96); border-bottom: 1px solid #d9e2ef; padding: 12px 18px; backdrop-filter: blur(8px); }}
    .toolbar-inner {{ max-width: 1120px; margin: 0 auto; display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center; }}
    input {{ width: 100%; height: 42px; border: 1px solid #c8d3e2; border-radius: 8px; padding: 0 12px; font-size: 15px; background: #fff; }}
    .count {{ color: #516178; font-size: 14px; white-space: nowrap; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 18px; }}
    .unit-nav {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }}
    .unit-btn {{ border: 1px solid #c8d3e2; background: #fff; color: #30415d; border-radius: 6px; min-height: 34px; padding: 0 12px; font-weight: 700; cursor: pointer; }}
    .unit-btn.active {{ background: #2f6fbd; border-color: #2f6fbd; color: #fff; }}
    .section-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin: 18px 0 10px; }}
    .section-head h2 {{ margin: 0; font-size: 21px; color: #172033; }}
    .section-head span {{ color: #6b7890; font-size: 13px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 12px; }}
    article {{ background: #fff; border: 1px solid #dce4ef; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(14, 31, 53, .04); }}
    .top {{ display: flex; justify-content: space-between; gap: 10px; align-items: start; }}
    .title-row {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
    h3 {{ margin: 0; font-size: 21px; color: #172033; letter-spacing: 0; }}
    .badge {{ display: inline-flex; min-height: 24px; border-radius: 6px; align-items: center; background: #e9eef7; color: #30415d; font-weight: 700; font-size: 12px; padding: 0 8px; }}
    .num {{ color: #6b7890; font-size: 13px; }}
    .pron {{ margin-top: 4px; color: #6b7890; font-size: 13px; }}
    .word-forms {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }}
    .wf {{ font-size: 12px; background: #edf2f7; color: #4a5568; border-radius: 4px; padding: 2px 8px; }}
    .wf em {{ color: #2b6cb0; font-style: normal; font-weight: 700; margin-right: 3px; }}
    .meaning {{ margin-top: 12px; font-size: 15px; color: #24344d; }}
    .explanation {{ margin-top: 10px; padding: 10px; border-radius: 6px; background: #f7fafc; color: #34445c; font-size: 14px; line-height: 1.58; }}
    .label {{ margin-top: 13px; font-size: 12px; font-weight: 700; color: #2f6fbd; text-transform: uppercase; }}
    .example {{ margin-top: 6px; font-size: 13px; color: #26344b; line-height: 1.5; }}
    .example span {{ display: block; color: #748196; margin-top: 2px; }}
    .related {{ display: grid; gap: 8px; margin-top: 8px; }}
    .related-item {{ border: 1px solid #e3eaf4; border-radius: 8px; padding: 10px; background: #fbfdff; }}
    .related-head {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; font-size: 13px; }}
    .related-head strong {{ color: #172033; }}
    .related-meaning {{ margin-top: 5px; color: #4a5870; font-size: 12px; line-height: 1.45; }}
    .related-example {{ margin-top: 5px; color: #26344b; font-size: 12px; line-height: 1.45; }}
    .related-example span {{ display: block; color: #748196; margin-top: 2px; }}
    .speak {{ flex: 0 0 auto; border: 1px solid #c8d3e2; background: #fff; color: #2f6fbd; border-radius: 999px; width: 28px; height: 28px; cursor: pointer; font-size: 13px; line-height: 1; display: inline-flex; align-items: center; justify-content: center; }}
    .speak:hover {{ background: #eef4ff; border-color: #2f6fbd; }}
    .speak.playing {{ background: #2f6fbd; color: #fff; border-color: #2f6fbd; }}
    @media (max-width: 640px) {{
      h1 {{ font-size: 23px; }}
      .toolbar-inner {{ grid-template-columns: 1fr; }}
      main {{ padding: 12px; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Language Summary Vocabulary</h1>
      <p class="sub">유닛별 핵심 단어 · 뜻, 품사, 예문, 유의어, TTS · {generated}</p>
    </div>
  </header>
  <div class="toolbar">
    <div class="toolbar-inner">
      <input id="search" type="search" placeholder="단어, 뜻, 예문으로 검색">
      <div class="count" id="count">0 / {total}</div>
    </div>
  </div>
  <main>
    <nav class="unit-nav" id="unit-nav" aria-label="유닛 선택"></nav>
    <div id="content"></div>
  </main>
  <script id="vocab-data" type="application/json">{data}</script>
  <script>
    const units = JSON.parse(document.getElementById('vocab-data').textContent);
    const unitNav = document.getElementById('unit-nav');
    const content = document.getElementById('content');
    const search = document.getElementById('search');
    const count = document.getElementById('count');
    let activeUnit = 0;

    function esc(value) {{
      return String(value || '').replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
    }}

    function wordCard(word) {{
      return `
        <article>
          <div class="top">
            <div>
              <div class="title-row">
                <h3>${{esc(word.word)}}</h3>
                <button class="speak" data-speak="${{esc(word.word.replace(/[()]/g, ''))}}" title="단어 발음 듣기" aria-label="단어 발음 듣기">🔊</button>
              </div>
              ${{word.pronunciation ? `<div class="pron">${{esc(word.pronunciation)}}</div>` : ''}}
            </div>
            <div>
              <div class="badge">${{esc(word.pos_ko)}}</div>
              <div class="num">#${{esc(word.number)}}</div>
            </div>
          </div>
          ${{word.word_forms && Object.keys(word.word_forms).length ? `
            <div class="word-forms">
              ${{word.word_forms.verb ? `<span class="wf"><em>v.</em> ${{esc(word.word_forms.verb)}}</span>` : ''}}
              ${{word.word_forms.noun ? `<span class="wf"><em>n.</em> ${{esc(word.word_forms.noun)}}</span>` : ''}}
              ${{word.word_forms.adjective ? `<span class="wf"><em>adj.</em> ${{esc(word.word_forms.adjective)}}</span>` : ''}}
              ${{word.word_forms.adverb ? `<span class="wf"><em>adv.</em> ${{esc(word.word_forms.adverb)}}</span>` : ''}}
            </div>
          ` : ''}}
          <div class="meaning"><strong>뜻:</strong> ${{esc(word.meaning_ko)}}</div>
          <div class="explanation">💡 ${{esc(word.explanation)}}</div>
          ${{word.examples && word.examples.length ? `
            <div class="label">Examples</div>
            ${{word.examples.map(ex => `
              <div class="example">
                <button class="speak" data-speak="${{esc(ex.en)}}" title="예문 발음 듣기" aria-label="예문 발음 듣기">🔊</button>
                "${{esc(ex.en)}}"
                <span>→ ${{esc(ex.ko)}}</span>
              </div>
            `).join('')}}
          ` : ''}}
          ${{word.synonyms.length ? `<div class="label">Similar</div>${{relatedList(word.synonyms)}}` : ''}}
          ${{word.antonyms.length ? `<div class="label">Opposite</div>${{relatedList(word.antonyms)}}` : ''}}
        </article>
      `;
    }}

    function relatedList(items) {{
      return `
        <div class="related">
          ${{items.map(item => `
            <div class="related-item">
              <div class="related-head">
                <button class="speak" data-speak="${{esc(item.en)}}" title="관련 표현 발음 듣기" aria-label="관련 표현 발음 듣기">🔊</button>
                <strong>${{esc(item.en)}}</strong>
              </div>
              <div class="related-meaning">${{esc(item.ko)}}</div>
              ${{item.example ? `
                <div class="related-example">
                  <button class="speak" data-speak="${{esc(item.example.en)}}" title="관련 예문 발음 듣기" aria-label="관련 예문 발음 듣기">🔊</button>
                  "${{esc(item.example.en)}}"
                  <span>→ ${{esc(item.example.ko)}}</span>
                </div>
              ` : ''}}
            </div>
          `).join('')}}
        </div>
      `;
    }}

    function render() {{
      const q = search.value.trim().toLowerCase();
      const unit = units[activeUnit];
      let visible = 0;
      const html = unit.sections.map(section => {{
        const words = section.words.filter(word => !q || JSON.stringify(word).toLowerCase().includes(q));
        visible += words.length;
        if (!words.length) return '';
        return `
          <section>
            <div class="section-head">
              <h2>${{esc(section.title)}}</h2>
              <span>${{words.length}} words</span>
            </div>
            <div class="grid">${{words.map(wordCard).join('')}}</div>
          </section>
        `;
      }}).join('');
      content.innerHTML = html || '<p>검색 결과가 없습니다.</p>';
      const total = unit.sections.reduce((sum, section) => sum + section.words.length, 0);
      count.textContent = `${{visible}} / ${{total}}`;
    }}

    function renderUnitNav() {{
      unitNav.innerHTML = units.map((unit, idx) => `
        <button class="unit-btn ${{idx === activeUnit ? 'active' : ''}}" data-unit="${{idx}}" aria-current="${{idx === activeUnit ? 'page' : 'false'}}">
          ${{esc(unit.title)}}
        </button>
      `).join('');
    }}

    unitNav.addEventListener('click', event => {{
      const button = event.target.closest('[data-unit]');
      if (!button) return;
      activeUnit = Number(button.dataset.unit);
      search.value = '';
      renderUnitNav();
      render();
    }});

    search.addEventListener('input', render);

    let currentBtn = null;
    document.addEventListener('click', event => {{
      const btn = event.target.closest('[data-speak]');
      if (!btn || typeof speechSynthesis === 'undefined') return;
      const text = btn.dataset.speak;
      speechSynthesis.cancel();
      if (currentBtn) currentBtn.classList.remove('playing');
      btn.classList.add('playing');
      currentBtn = btn;
      setTimeout(() => {{
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.onend = () => {{ btn.classList.remove('playing'); currentBtn = null; }};
        utterance.onerror = () => {{ btn.classList.remove('playing'); currentBtn = null; }};
        speechSynthesis.speak(utterance);
      }}, 50);
    }});

    renderUnitNav();
    render();
  </script>
</body>
</html>"""


def build():
    source_path = os.path.join(BASE_DIR, "language_summary_vocabulary.md")
    output_path = os.path.join(BASE_DIR, "docs", "language-summary-vocabulary.html")
    units = parse_markdown(source_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(render_html(units))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    build()
