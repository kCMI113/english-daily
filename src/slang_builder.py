import json
import os
import re
from datetime import date


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


PRONUNCIATION = {
    "Addy": "애디",
    "Amirite": "어마이롸잇",
    "Amped": "앰프트",
    "Aura": "오라",
    "Bae": "베이",
    "Bandwagon": "밴드왜건",
    "Basic": "베이식",
    "Bed rot": "베드 롯",
    "Bet": "벳",
    "Boomer / Okay Boomer": "부머 / 오케이 부머",
    "Boujee": "부지",
    "Bussin'": "버신",
    "Cap": "캡",
    "Cash": "캐시",
    "Catch feels": "캐치 필즈",
    "Caught in 4k": "콧 인 포케이",
    "Chat": "챗",
    "Cheugy": "추기",
    "Cooked": "쿡트",
    "Cringe": "크린지",
    "Dank": "댕크",
    "Dip": "딥",
    "DL": "디엘",
    "Dope": "도프",
    "Dox": "독스",
    "Drag": "드래그",
    "Drip": "드립",
    "Dub": "덥",
    "Egirl / Eboy": "이걸 / 이보이",
    "Extra": "엑스트라",
    "Facts": "팩츠",
    "Faded": "페이디드",
    "Fan service": "팬 서비스",
    "Finna": "피나",
    "Finsta": "핀스타",
    "Fire": "파이어",
    "Fit": "핏",
    "Flex": "플렉스",
    "FR": "에프알",
    "FRFR": "에프알에프알",
    "FYP": "에프와이피",
    "Gassing": "개싱",
    "Ghost": "고스트",
    "Giving me life": "기빙 미 라이프",
    "Glow-up": "글로우 업",
    "GOAT": "고트",
    "Granola": "그래놀라",
    "Guap": "괍",
    "Gucci": "구치",
    "Hammered": "해머드",
    "Heated": "히티드",
    "Here for this": "히어 포 디스",
    "High key": "하이 키",
    "Hits different": "히츠 디퍼런트",
    "Hollywood": "할리우드",
    "Hop off": "홉 오프",
    "Hot take": "핫 테이크",
    "Hype": "하이프",
    "Ick": "익",
    "ICYMI": "아이씨와이엠아이",
    "IRL": "아이알엘",
    "IYKYK": "아이와이케이와이케이",
    "Juul": "줄",
    "Keep it 100": "킵 잇 원헌드레드",
    "L": "엘",
    "Left on read": "레프트 온 레드",
    "Lit": "릿",
    "LMAO": "엘엠에이오",
    "LMS": "엘엠에스",
    "LOL": "엘오엘",
    "Mad": "매드",
    "Mid": "미드",
    "Netflix and chill": "넷플릭스 앤 칠",
    "NGL": "엔지엘",
    "NSFW": "엔에스에프더블유",
    "OMG": "오엠지",
    "OML": "오엠엘",
    "OMW": "오엠더블유",
    "ONG": "온 갓",
    "On fleek": "온 플릭",
    "On point": "온 포인트",
    "Only in Ohio": "온리 인 오하이오",
    "OTP": "오티피",
    "Periodt": "피리어트",
    "Pressed": "프레스트",
    "Pulling": "풀링",
    "Put on blast": "풋 온 블래스트",
    "Rad": "래드",
    "Real": "리얼",
    "Receipts": "리시츠",
    "Rent free": "렌트 프리",
    "Rizz": "리즈",
    "RN": "알엔",
    "Salty": "솔티",
    "Savage": "새비지",
    "Say less": "세이 레스",
    "Sending me": "센딩 미",
    "Shade": "셰이드",
    "Ship": "십",
    "Shook": "슉",
    "Shorty": "쇼티",
    "Sick": "식",
    "Simp": "심프",
    "Skibidi Toilet": "스키비디 토일럿",
    "Slap": "슬랩",
    "Slay": "슬레이",
    "SMH": "에스엠에이치",
    "S/O / SO": "에스오",
    "Stan": "스탠",
    "Stoked": "스토크트",
    "Sus": "서스",
    "Swerve": "스워브",
    "Swole": "스월",
    "Swoop": "스웁",
    "Take a seat": "테이크 어 시트",
    "Tea": "티",
    "TFW": "티에프더블유",
    "Thirsty": "서스티",
    "Thirst Trap": "서스트 트랩",
    "Touch grass": "터치 그래스",
    "Twin": "트윈",
    "Twizzy": "트위지",
    "Unc": "엉크",
    "Understood the assignment": "언더스투드 디 어사인먼트",
    "V": "브이",
    "Vanilla": "바닐라",
    "Vibe": "바이브",
    "VSCO girl": "비스코 걸",
    "W": "더블유",
    "Wallflower": "월플라워",
    "Whip": "윕",
    "Woke": "워크",
    "WYA": "더블유와이에이",
    "Yeet": "윳",
    "Zaddy": "재디",
}


KO = {
    "Addy": "주소를 짧고 가볍게 부르는 말입니다. 문자나 디엠에서 약속 장소를 알려 달라고 할 때 자주 씁니다.",
    "Amirite": "내 말 맞지? 정도의 장난스러운 확인 표현입니다. 격식 있는 상황보다는 친구 사이 농담에 어울립니다.",
    "Amped": "무언가를 앞두고 들뜨고 기대되는 상태를 말합니다. excited보다 더 에너지가 넘치는 느낌입니다.",
    "Aura": "사람에게서 느껴지는 멋, 존재감, 압도적인 분위기를 칭찬할 때 씁니다.",
    "Bae": "연인이나 아주 아끼는 사람을 부르는 애칭입니다. 다만 지금은 다소 유행이 지난 느낌도 있습니다.",
    "Bandwagon": "진짜 관심보다 유행에 맞추려고 따라붙는 사람이나 태도를 말합니다.",
    "Basic": "개성이 없고 유행하는 것만 따라 하는 느낌을 가볍게 비꼴 때 씁니다.",
    "Bed rot": "침대에 오래 누워 휴대폰, 영상, 독서 등을 하며 쉬는 행동입니다. 자기관리 부족을 비판할 때도 쓰입니다.",
    "Bet": "좋아, 알겠어, 그렇게 하자라는 동의 표현입니다. 짧고 캐주얼합니다.",
    "Boomer / Okay Boomer": "기성세대식 잔소리나 낡은 태도를 비꼬며 받아치는 표현입니다. 무례하게 들릴 수 있습니다.",
    "Boujee": "비싸고 고급스럽거나 허세 섞인 럭셔리한 분위기를 말합니다.",
    "Bussin'": "음식이나 노래처럼 무언가가 정말 좋을 때 쓰는 강한 칭찬입니다.",
    "Cap": "거짓말이나 허풍을 뜻합니다. no cap은 진짜야, 거짓말 아냐라는 뜻입니다.",
    "Cash": "멋지다, 좋다라는 뜻의 오래된 캐주얼 표현입니다. 현재는 지역이나 세대에 따라 덜 자연스러울 수 있습니다.",
    "Catch feels": "누군가에게 감정이 생기거나 좋아하는 마음이 커지는 것을 말합니다.",
    "Caught in 4k": "잘못하거나 민망한 행동을 아주 확실한 증거와 함께 들켰다는 뜻입니다.",
    "Chat": "라이브 방송이나 온라인 대화에서 청중, 친구들, 여러분 정도로 부르는 말입니다.",
    "Cheugy": "한때 유행했지만 지금은 촌스럽거나 애써 멋 부리는 느낌을 말합니다.",
    "Cooked": "너무 지쳤거나 상황이 망했다는 뜻입니다. 시험, 경기, 일상 상황에 두루 씁니다.",
    "Cringe": "민망하고 보기 불편한 느낌을 말합니다. 사람이나 상황을 평가할 때 자주 씁니다.",
    "Dank": "아주 좋고 질이 높다는 뜻입니다. 음식, 밈, 파티 등에 쓰입니다.",
    "Dip": "갑자기 또는 일찍 자리를 뜨다라는 뜻입니다.",
    "DL": "down low의 줄임말로, 비밀로 하거나 조용히 처리한다는 뜻입니다.",
    "Dope": "멋지고 훌륭하다는 뜻의 칭찬입니다. 사물, 음악, 아이디어에 널리 씁니다.",
    "Dox": "타인의 개인정보를 악의적으로 찾아 공개하는 행위입니다. 심각한 온라인 괴롭힘에 해당합니다.",
    "Drag": "상대를 공개적으로 조롱하거나 강하게 비판한다는 뜻입니다.",
    "Drip": "옷차림이나 스타일이 세련되고 멋지다는 뜻입니다.",
    "Dub": "승리, 성공을 뜻하는 W에서 온 말입니다.",
    "Egirl / Eboy": "틱톡 등 온라인 문화에서 보이는 대안적이고 엣지 있는 스타일의 사람을 말합니다.",
    "Extra": "행동이나 반응이 과하게 극적이고 눈에 띈다는 뜻입니다.",
    "Facts": "맞아, 인정이라는 강한 동의 표현입니다.",
    "Faded": "술이나 약물에 취한 상태를 말합니다. 민감한 맥락이므로 사용에 주의가 필요합니다.",
    "Fan service": "팬들이 좋아할 만한 장면, 농담, 설정을 작품에 넣는 것을 말합니다.",
    "Finna": "going to, about to와 비슷하게 곧 무엇을 할 것이라는 뜻입니다. AAVE에서 온 표현입니다.",
    "Finsta": "친한 사람에게만 보여주는 비공개 또는 보조 인스타그램 계정을 말합니다.",
    "Fire": "정말 멋지거나 훌륭하다는 뜻입니다.",
    "Fit": "outfit의 줄임말로 옷차림을 뜻합니다.",
    "Flex": "돈, 물건, 능력 등을 과시한다는 뜻입니다.",
    "FR": "for real의 줄임말로, 진짜로 또는 인정이라는 뜻입니다.",
    "FRFR": "for real for real의 줄임말로 진심임을 더 강하게 강조합니다.",
    "FYP": "틱톡의 추천 피드인 For You Page를 뜻합니다.",
    "Gassing": "상대방을 과하게 띄워 주거나 치켜세우는 것을 말합니다.",
    "Ghost": "설명 없이 연락을 끊는 행동입니다.",
    "Giving me life": "무언가가 너무 즐겁고 기분을 살려 준다는 뜻입니다.",
    "Glow-up": "외모나 분위기가 크게 좋아진 변화를 말합니다.",
    "GOAT": "greatest of all time의 줄임말로 역대 최고라는 극찬입니다.",
    "Granola": "자연친화적이고 야외 활동을 좋아하는 사람을 가리키는 말입니다.",
    "Guap": "많은 돈을 뜻하는 속어입니다.",
    "Gucci": "좋아, 문제없어, 멋지다라는 뜻으로 씁니다.",
    "Hammered": "술이나 약물에 많이 취한 상태를 말합니다.",
    "Heated": "화가 나거나 감정이 격해진 상태입니다.",
    "Here for this": "그 상황이나 선택을 적극 지지하고 좋게 본다는 뜻입니다.",
    "High key": "low key의 반대로, 숨기지 않고 꽤 강하게 그렇다는 뜻입니다.",
    "Hits different": "특별하게 와닿거나 평소와 다르게 강한 감정을 준다는 뜻입니다.",
    "Hollywood": "성공 후 변해서 거만해졌다는 부정적 표현입니다.",
    "Hop off": "그만 괴롭혀, 참견하지 마라는 뜻의 날카로운 표현입니다.",
    "Hot take": "논쟁적이거나 과감한 의견을 말합니다.",
    "Hype": "신나고 기대되거나 분위기가 뜨거운 상태입니다.",
    "Ick": "상대에게 갑자기 정이 떨어지는 불쾌 포인트를 말합니다.",
    "ICYMI": "in case you missed it의 줄임말로 혹시 못 봤다면이라는 뜻입니다.",
    "IRL": "in real life의 줄임말로 온라인이 아닌 현실에서라는 뜻입니다.",
    "IYKYK": "if you know, you know의 줄임말로 아는 사람만 아는 내부 농담이나 경험을 가리킵니다.",
    "Juul": "전자담배 브랜드명입니다. 일반적으로 전자담배를 가리키는 말처럼 쓰이기도 합니다.",
    "Keep it 100": "항상 솔직하고 진정성 있게 말하거나 행동한다는 뜻입니다.",
    "L": "loss의 줄임말로 실패나 패배를 뜻합니다.",
    "Left on read": "메시지를 읽고 답장을 하지 않은 상태입니다.",
    "Lit": "재밌고 신나거나 아주 좋다는 뜻입니다. 취했다는 뜻도 있습니다.",
    "LMAO": "laughing my ass off의 줄임말로 아주 웃기다는 뜻입니다.",
    "LMS": "like my status의 줄임말로 게시물에 좋아요를 눌러 달라는 뜻입니다.",
    "LOL": "laugh out loud의 줄임말로 웃기다, 웃음 정도의 반응입니다.",
    "Mad": "very처럼 정말, 엄청이라는 강조 부사로도 쓰입니다.",
    "Mid": "평범하거나 기대 이하라는 평가입니다.",
    "Netflix and chill": "겉으로는 영상을 보자는 말이지만, 보통 성적 만남을 완곡하게 뜻합니다.",
    "NGL": "not gonna lie의 줄임말로 솔직히 말하면이라는 뜻입니다.",
    "NSFW": "not safe for work의 줄임말로 공공장소나 직장에서 보기 부적절한 콘텐츠를 뜻합니다.",
    "OMG": "oh my God 또는 oh my gosh의 줄임말로 놀람을 나타냅니다.",
    "OML": "oh my Lord의 줄임말로 놀람이나 흥분을 나타냅니다.",
    "OMW": "on my way의 줄임말로 가는 중이라는 뜻입니다.",
    "ONG": "on God의 줄임말로 맹세코 진짜라는 강한 동의나 확신을 나타냅니다.",
    "On fleek": "외모나 스타일이 완벽하게 잘됐다는 뜻입니다. 요즘은 다소 예전 유행처럼 들릴 수 있습니다.",
    "On point": "정확하고 훌륭하며 딱 맞는다는 뜻입니다.",
    "Only in Ohio": "이상하고 말도 안 되는 상황을 밈처럼 놀릴 때 쓰는 표현입니다.",
    "OTP": "one true pairing의 줄임말로 가장 좋아하는 커플 조합을 뜻합니다.",
    "Periodt": "더 말할 필요 없이 끝이라는 식으로 단호하게 마무리할 때 씁니다.",
    "Pressed": "사소한 일에 예민하게 짜증 내거나 스트레스받는 상태입니다.",
    "Pulling": "이성의 관심을 끌거나 성공적으로 호감을 얻는다는 뜻입니다.",
    "Put on blast": "누군가의 잘못을 공개적으로 폭로하거나 망신을 주는 것입니다.",
    "Rad": "멋지다, 훌륭하다는 오래된 캐주얼 표현입니다.",
    "Real": "진지하게, 정말로라는 뜻입니다. be so for real처럼 상대를 현실적으로 보라고 할 때 씁니다.",
    "Receipts": "말이나 행동을 증명하는 캡처, 기록, 증거를 뜻합니다.",
    "Rent free": "어떤 사람이나 일이 머릿속에서 계속 떠나지 않는다는 뜻입니다.",
    "Rizz": "상대를 끌어당기는 매력이나 플러팅 능력을 뜻합니다.",
    "RN": "right now의 줄임말로 지금 당장이라는 뜻입니다.",
    "Salty": "삐치거나 억울해하며 짜증 난 상태입니다.",
    "Savage": "거침없고 대담하거나 냉정하게 잘 받아치는 사람을 말합니다.",
    "Say less": "더 설명하지 않아도 알겠다는 뜻입니다.",
    "Sending me": "너무 웃겨서 나를 보내 버린다는 식의 강한 웃음 반응입니다.",
    "Shade": "노골적이지 않게 깎아내리거나 비꼬는 말입니다.",
    "Ship": "두 사람의 연애 관계를 응원한다는 뜻입니다.",
    "Shook": "매우 놀라거나 충격받은 상태입니다.",
    "Shorty": "매력적인 여성을 부르는 속어입니다. 상황에 따라 무례하게 들릴 수 있습니다.",
    "Sick": "아프다는 뜻 외에 멋지다, 대단하다는 뜻으로도 씁니다.",
    "Simp": "상대에게 과하게 매달리거나 비굴하게 호감을 구하는 사람을 낮춰 부르는 말입니다.",
    "Skibidi Toilet": "유튜브 밈 콘텐츠명입니다. 표현 자체보다 밈 문화의 참조로 보는 것이 정확합니다.",
    "Slap": "노래나 음식 등이 정말 좋다는 뜻입니다.",
    "Slay": "무언가를 아주 잘 해냈다는 칭찬입니다.",
    "SMH": "shaking my head의 줄임말로 어이없거나 한심하다는 반응입니다.",
    "S/O / SO": "S/O는 shout out, SO는 significant other로 쓰이는 경우가 많습니다. 원문 의미를 살리되 표기를 구분했습니다.",
    "Stan": "특정 인물이나 작품을 열성적으로 좋아하는 팬을 뜻합니다.",
    "Stoked": "매우 신나고 기대되는 상태입니다.",
    "Sus": "suspicious의 줄임말로 수상하다는 뜻입니다.",
    "Swerve": "누군가를 의도적으로 피한다는 뜻입니다.",
    "Swole": "근육이 크고 몸이 탄탄하다는 뜻입니다.",
    "Swoop": "차로 데리러 가거나 태워 준다는 뜻입니다.",
    "Take a seat": "진정하고 그만하라는 식의 비꼬는 말입니다.",
    "Tea": "소문이나 뒷이야기를 뜻합니다. spill the tea는 소문을 말하다입니다.",
    "TFW": "that feeling when의 줄임말로 어떤 상황의 감정을 설명할 때 씁니다.",
    "Thirsty": "관심이나 인정, 호감을 지나치게 갈구하는 상태입니다.",
    "Thirst Trap": "관심을 끌려고 올리는 도발적인 사진이나 영상입니다.",
    "Touch grass": "온라인에서 벗어나 현실을 좀 살라는 뜻의 비꼬는 조언입니다.",
    "Twin": "취향이나 경험이 비슷한 아주 가까운 친구를 부르는 말입니다.",
    "Twizzy": "twin의 변형으로 가까운 친구를 부르는 말입니다.",
    "Unc": "uncle의 줄임말로 나이 든 느낌이 나거나 살짝 윗세대를 가리킬 때 씁니다.",
    "Understood the assignment": "기대 이상으로 잘 해냈다는 칭찬입니다.",
    "V": "very의 줄임말로 문자에서 가볍게 강조할 때 씁니다.",
    "Vanilla": "평범하고 특별한 맛이 없다는 뜻입니다.",
    "Vibe": "사람이나 장소에서 느껴지는 분위기입니다.",
    "VSCO girl": "특정 앱과 패션 소품으로 대표되는 2010년대 후반 온라인 스타일입니다.",
    "W": "win의 줄임말로 승리나 좋은 결과를 뜻합니다.",
    "Wallflower": "사교 상황에서 눈에 띄기보다 조용히 있는 사람입니다.",
    "Whip": "차, 특히 멋진 차를 뜻하는 속어입니다.",
    "Woke": "사회 문제에 깨어 있다는 뜻입니다. 비꼬는 의미로도 쓰입니다.",
    "WYA": "where you at의 줄임말로 어디야?라는 문자 표현입니다.",
    "Yeet": "무언가를 힘껏 던지다라는 뜻입니다.",
    "Zaddy": "나이 있고 세련되며 매력적인 남성을 가리키는 말입니다.",
}


SIMILAR = {
    "Addy": ["address", "location", "where you at"],
    "Amirite": ["right?", "isn't it?", "you know?"],
    "Amped": ["hyped", "stoked", "excited"],
    "Aura": ["presence", "vibe", "energy"],
    "Bae": ["babe", "boo", "significant other"],
    "Bandwagon": ["trend follower", "fair-weather fan"],
    "Basic": ["mainstream", "unoriginal", "vanilla"],
    "Bed rot": ["doomscroll", "veg out", "rot day"],
    "Bet": ["okay", "say less", "for sure"],
    "Boomer / Okay Boomer": ["out of touch", "old-school"],
    "Boujee": ["fancy", "luxury", "posh"],
    "Bussin'": ["fire", "slaps", "delicious"],
    "Cap": ["lie", "fake", "no cap"],
    "Cash": ["cool", "dope", "rad"],
    "Catch feels": ["fall for", "get attached", "develop feelings"],
    "Caught in 4k": ["exposed", "busted", "caught red-handed"],
    "Chat": ["guys", "everyone", "stream"],
    "Cheugy": ["outdated", "cringe", "trying too hard"],
    "Cooked": ["done", "finished", "toast"],
    "Cringe": ["awkward", "embarrassing", "secondhand embarrassment"],
    "Dank": ["excellent", "fire", "top-tier"],
    "Dip": ["leave", "bounce", "head out"],
    "DL": ["secret", "low-key", "under wraps"],
    "Dope": ["cool", "fire", "sick"],
    "Dox": ["expose private info", "leak personal info"],
    "Drag": ["roast", "mock", "call out"],
    "Drip": ["style", "fit", "swag"],
    "Dub": ["W", "win", "victory"],
    "Egirl / Eboy": ["alt style", "TikTok aesthetic"],
    "Extra": ["dramatic", "over the top", "too much"],
    "Facts": ["true", "exactly", "FR"],
    "Faded": ["high", "stoned", "intoxicated"],
    "Fan service": ["easter egg", "inside joke", "nod to fans"],
    "Finna": ["gonna", "about to", "fixing to"],
    "Finsta": ["private Instagram", "alt account"],
    "Fire": ["amazing", "dope", "lit"],
    "Fit": ["outfit", "look", "drip"],
    "Flex": ["show off", "brag", "flaunt"],
    "FR": ["for real", "facts", "seriously"],
    "FRFR": ["dead serious", "for real", "no joke"],
    "FYP": ["For You Page", "feed", "recommendations"],
    "Gassing": ["hyping up", "overpraising", "boosting"],
    "Ghost": ["ignore", "cut off", "disappear"],
    "Giving me life": ["energizing", "making my day", "so good"],
    "Glow-up": ["transformation", "upgrade", "level up"],
    "GOAT": ["best ever", "legend", "all-time great"],
    "Granola": ["outdoorsy", "eco-conscious", "crunchy"],
    "Guap": ["money", "cash", "stack"],
    "Gucci": ["all good", "cool", "fine"],
    "Hammered": ["wasted", "drunk", "intoxicated"],
    "Heated": ["angry", "mad", "worked up"],
    "Here for this": ["I support it", "love this", "I'm into it"],
    "High key": ["openly", "honestly", "very"],
    "Hits different": ["special", "stands out", "feels different"],
    "Hollywood": ["changed up", "acting superior", "too big for themself"],
    "Hop off": ["back off", "leave alone", "stop bothering"],
    "Hot take": ["controversial opinion", "bold take"],
    "Hype": ["excited", "lit", "energetic"],
    "Ick": ["turnoff", "red flag", "gross feeling"],
    "ICYMI": ["in case you missed it", "FYI"],
    "IRL": ["in real life", "offline"],
    "IYKYK": ["inside joke", "you had to be there"],
    "Juul": ["vape", "e-cigarette"],
    "Keep it 100": ["be real", "be honest", "keep it real"],
    "L": ["loss", "fail", "defeat"],
    "Left on read": ["ignored", "no reply", "seen-zoned"],
    "Lit": ["exciting", "fire", "hype"],
    "LMAO": ["LOL", "ROFL", "I'm dying"],
    "LMS": ["like my status", "like this post"],
    "LOL": ["haha", "lmao", "laughing"],
    "Mad": ["very", "super", "really"],
    "Mid": ["average", "meh", "not great"],
    "Netflix and chill": ["hook up", "come over"],
    "NGL": ["not gonna lie", "honestly", "to be honest"],
    "NSFW": ["explicit", "inappropriate", "adult content"],
    "OMG": ["oh my gosh", "wow", "no way"],
    "OML": ["oh my Lord", "OMG", "wow"],
    "OMW": ["on my way", "headed there"],
    "ONG": ["I swear", "for real", "on God"],
    "On fleek": ["perfect", "flawless", "on point"],
    "On point": ["perfect", "spot-on", "exactly right"],
    "Only in Ohio": ["cursed", "weird", "absurd"],
    "OTP": ["favorite couple", "ship", "pairing"],
    "Periodt": ["period", "end of story", "that's final"],
    "Pressed": ["annoyed", "upset", "bothered"],
    "Pulling": ["attracting", "getting attention", "rizzing"],
    "Put on blast": ["expose", "call out", "publicly shame"],
    "Rad": ["cool", "awesome", "sick"],
    "Real": ["serious", "for real", "be honest"],
    "Receipts": ["proof", "screenshots", "evidence"],
    "Rent free": ["can't stop thinking", "stuck in my head"],
    "Rizz": ["charm", "game", "charisma"],
    "RN": ["right now", "currently"],
    "Salty": ["bitter", "resentful", "pressed"],
    "Savage": ["bold", "ruthless", "brutal"],
    "Say less": ["got it", "bet", "I understand"],
    "Sending me": ["cracking me up", "I'm dying", "so funny"],
    "Shade": ["subtle insult", "dig", "side-eye"],
    "Ship": ["support a couple", "pair", "root for"],
    "Shook": ["shocked", "stunned", "surprised"],
    "Shorty": ["girl", "baddie", "bae"],
    "Sick": ["cool", "awesome", "dope"],
    "Simp": ["try-hard admirer", "overly devoted"],
    "Skibidi Toilet": ["meme", "Gen Alpha meme", "internet series"],
    "Slap": ["be great", "hit hard", "fire"],
    "Slay": ["nail it", "crush it", "kill it"],
    "SMH": ["shaking my head", "facepalm"],
    "S/O / SO": ["shout out", "significant other"],
    "Stan": ["superfan", "obsessive fan", "supporter"],
    "Stoked": ["excited", "amped", "hyped"],
    "Sus": ["suspicious", "sketchy", "shady"],
    "Swerve": ["avoid", "dodge", "duck"],
    "Swole": ["muscular", "jacked", "buff"],
    "Swoop": ["pick up", "give a ride", "come get"],
    "Take a seat": ["calm down", "sit down", "stop talking"],
    "Tea": ["gossip", "drama", "spilling details"],
    "TFW": ["that feeling when", "mood"],
    "Thirsty": ["desperate", "attention-seeking", "needy"],
    "Thirst Trap": ["provocative post", "attention bait"],
    "Touch grass": ["go outside", "log off", "get offline"],
    "Twin": ["bestie", "close friend", "same person"],
    "Twizzy": ["twin", "bestie", "close friend"],
    "Unc": ["uncle", "older guy", "old head"],
    "Understood the assignment": ["nailed it", "delivered", "crushed it"],
    "V": ["very", "super", "really"],
    "Vanilla": ["plain", "ordinary", "basic"],
    "Vibe": ["energy", "mood", "atmosphere"],
    "VSCO girl": ["VSCO aesthetic", "trend girl"],
    "W": ["win", "dub", "victory"],
    "Wallflower": ["introvert", "quiet person", "observer"],
    "Whip": ["car", "ride", "vehicle"],
    "Woke": ["socially aware", "progressive", "politically aware"],
    "WYA": ["where are you", "where you at"],
    "Yeet": ["throw", "hurl", "launch"],
    "Zaddy": ["stylish older man", "silver fox"],
}


ADDED_EXAMPLES = {
    "Addy": ("Text me your addy before I leave.", "출발하기 전에 네 주소 문자로 보내 줘."),
    "Amirite": ("This line is way too long, amirite?", "이 줄 너무 길지, 내 말 맞지?"),
    "Amped": ("The team is amped for the finals.", "팀이 결승전을 앞두고 완전 들떠 있어."),
    "Aura": ("She walked in with serious main-character aura.", "그녀가 들어오는데 주인공 같은 존재감이 확 느껴졌어."),
    "Bae": ("I'm grabbing dinner with bae tonight.", "오늘 밤에 애인이랑 저녁 먹으러 가."),
    "Bandwagon": ("He only joined the bandwagon after they started winning.", "그 팀이 이기기 시작하니까 그제야 유행 따라 팬이 됐어."),
    "Basic": ("That caption is kind of basic, but it works.", "그 캡션 좀 흔하긴 한데 괜찮아."),
    "Bed rot": ("I spent Sunday bed rotting and watching old shows.", "일요일에는 침대에 누워 예전 드라마만 보면서 쉬었어."),
    "Bet": ("Bet, I'll send it over tonight.", "좋아, 오늘 밤에 보내 줄게."),
    "Boomer / Okay Boomer": ("He told us phones ruin everything, and someone whispered, 'Okay, boomer.'", "그가 휴대폰이 다 망친다고 하자 누군가 작게 '오케이 부머'라고 했어."),
    "Boujee": ("This cafe is cute, but the prices are boujee.", "이 카페 예쁘긴 한데 가격이 꽤 고급스럽네."),
    "Bussin'": ("These fries are bussin'.", "이 감자튀김 진짜 맛있다."),
    "Cap": ("You're saying you finished already? That's cap.", "벌써 끝냈다고? 그거 거짓말이지."),
    "Cash": ("That jacket is cash, but I wouldn't say it that way now.", "그 재킷 멋지긴 한데 요즘은 그렇게 말하진 않을 것 같아."),
    "Catch feels": ("I was just joking around, but I started to catch feels.", "장난으로 시작했는데 점점 마음이 생겼어."),
    "Caught in 4k": ("He denied it, but the screenshot had him caught in 4k.", "그는 부인했지만 캡처 때문에 제대로 들켰어."),
    "Chat": ("Chat, I need help choosing a movie.", "얘들아, 영화 고르는 거 좀 도와줘."),
    "Cheugy": ("That slogan feels a little cheugy now.", "그 문구는 이제 좀 촌스럽게 느껴져."),
    "Cooked": ("If I forget my notes, I'm cooked.", "노트를 까먹으면 나 망한 거야."),
    "Cringe": ("His fake accent was so cringe.", "그의 가짜 억양은 정말 민망했어."),
    "Dank": ("That playlist is dank.", "그 플레이리스트 진짜 좋다."),
    "Dip": ("The party got awkward, so we dipped.", "파티 분위기가 어색해져서 우리는 빠져나왔어."),
    "DL": ("Keep the plan on the DL until Friday.", "금요일까지 그 계획은 비밀로 해 둬."),
    "Dope": ("Your new setup looks dope.", "네 새 세팅 진짜 멋져 보여."),
    "Dox": ("Never dox someone just because you disagree with them.", "의견이 다르다고 누군가의 개인정보를 공개하면 절대 안 돼."),
    "Drag": ("The comments dragged him for that bad apology.", "댓글들이 그 형편없는 사과문 때문에 그를 심하게 비판했어."),
    "Drip": ("She showed up with serious drip.", "그녀가 엄청 스타일리시하게 나타났어."),
    "Dub": ("Finishing the project early was a dub.", "프로젝트를 일찍 끝낸 건 완전 성공이었어."),
    "Egirl / Eboy": ("His eyeliner gives the whole outfit an eboy vibe.", "그의 아이라이너가 전체 착장에 이보이 느낌을 줘."),
    "Extra": ("Bringing fireworks to a picnic is extra.", "소풍에 폭죽을 가져오는 건 너무 과해."),
    "Facts": ("Facts, that restaurant never misses.", "인정, 그 식당은 항상 맛있어."),
    "Faded": ("He looked faded, so his friends took him home.", "그가 취해 보여서 친구들이 집에 데려갔어."),
    "Fan service": ("That cameo was pure fan service.", "그 카메오는 완전 팬서비스였어."),
    "Finna": ("I'm finna leave in five minutes.", "나 5분 뒤에 나갈 거야."),
    "Finsta": ("She posts the messy photos on her finsta.", "그녀는 자연스럽고 꾸밈없는 사진을 비공개 계정에 올려."),
    "Fire": ("The new single is fire.", "새 싱글 진짜 좋다."),
    "Fit": ("Your fit is clean today.", "오늘 네 옷차림 깔끔하다."),
    "Flex": ("He bought one watch and started flexing online.", "그는 시계 하나 사더니 온라인에서 자랑하기 시작했어."),
    "FR": ("FR, I thought the test was impossible.", "진짜로, 그 시험 불가능한 줄 알았어."),
    "FRFR": ("I'm done arguing, FRFR.", "나 진짜로 이제 말싸움 그만할래."),
    "FYP": ("My FYP is full of cooking videos.", "내 추천 피드는 요리 영상으로 가득해."),
    "Gassing": ("Stop gassing me up; it was just a lucky shot.", "그만 띄워 줘. 그냥 운 좋게 들어간 슛이었어."),
    "Ghost": ("She ghosted the group chat for a week.", "그녀는 일주일 동안 단체 채팅에서 사라졌어."),
    "Giving me life": ("This sunny weather is giving me life.", "이 화창한 날씨가 기분을 확 살려 줘."),
    "Glow-up": ("His confidence had a real glow-up this year.", "올해 그는 자신감이 정말 많이 좋아졌어."),
    "GOAT": ("Serena is the GOAT to a lot of tennis fans.", "많은 테니스 팬에게 세리나는 역대 최고야."),
    "Granola": ("He's granola: hiking boots, reusable bottle, sunrise walks.", "그는 자연친화적인 스타일이야. 등산화, 재사용 물병, 해돋이 산책 같은 걸 좋아해."),
    "Guap": ("They spent serious guap on those concert tickets.", "그들은 그 콘서트 티켓에 돈을 꽤 많이 썼어."),
    "Gucci": ("Don't worry, we're gucci.", "걱정 마, 우리 괜찮아."),
    "Hammered": ("They were hammered after the wedding reception.", "그들은 결혼식 피로연 후에 많이 취했어."),
    "Heated": ("The debate got heated fast.", "토론이 금방 격해졌어."),
    "Here for this": ("A quiet office and free coffee? I'm here for this.", "조용한 사무실에 무료 커피라니, 난 완전 좋아."),
    "High key": ("I high key want to cancel and stay home.", "솔직히 나 취소하고 집에 있고 싶어."),
    "Hits different": ("Cold water after a long run hits different.", "오래 달린 뒤 마시는 찬물은 유난히 좋게 느껴져."),
    "Hollywood": ("He got one promotion and started acting Hollywood.", "그는 승진 한 번 하더니 거만하게 굴기 시작했어."),
    "Hop off": ("Hop off my playlist; I know it's good.", "내 플레이리스트 그만 뭐라 해. 좋은 거 나도 알아."),
    "Hot take": ("Hot take: the sequel is better than the original.", "과감한 의견인데, 속편이 원작보다 나아."),
    "Hype": ("The crowd got hype when the beat dropped.", "비트가 떨어지자 관중이 확 달아올랐어."),
    "Ick": ("Loud chewing gives me the ick.", "쩝쩝거리는 소리는 나를 확 정떨어지게 해."),
    "ICYMI": ("ICYMI, the meeting moved to 3 p.m.", "혹시 못 봤다면, 회의가 오후 3시로 옮겨졌어."),
    "IRL": ("She's even funnier IRL.", "그녀는 실제로 보면 더 웃겨."),
    "IYKYK": ("That tiny ramen shop near campus is perfect. IYKYK.", "캠퍼스 근처 그 작은 라멘집 완벽해. 아는 사람은 알지."),
    "Juul": ("The school banned Juuls on campus.", "학교는 캠퍼스 내 전자담배를 금지했어."),
    "Keep it 100": ("Keep it 100 with me: was my presentation boring?", "솔직히 말해 줘. 내 발표 지루했어?"),
    "L": ("Missing the deadline was a big L.", "마감일을 놓친 건 큰 실패였어."),
    "Left on read": ("I asked a simple question and got left on read.", "간단한 질문을 했는데 읽씹당했어."),
    "Lit": ("The after-party was lit.", "뒤풀이가 진짜 신났어."),
    "LMAO": ("LMAO, I can't believe you wore that hat.", "아 진짜 웃겨, 네가 그 모자를 썼다니 믿기지 않아."),
    "LMS": ("LMS if you want the recipe.", "레시피 원하면 좋아요 눌러."),
    "LOL": ("LOL, I sent the wrong file again.", "하하, 나 또 파일을 잘못 보냈어."),
    "Mad": ("That line was mad long.", "그 줄 진짜 길었어."),
    "Mid": ("The trailer looked amazing, but the movie was mid.", "예고편은 대단해 보였는데 영화는 그냥 그랬어."),
    "Netflix and chill": ("He said 'Netflix and chill,' but she knew what he meant.", "그가 넷플릭스 보자고 했지만 그녀는 숨은 뜻을 알았어."),
    "NGL": ("NGL, I liked the old design better.", "솔직히 말하면 예전 디자인이 더 좋았어."),
    "NSFW": ("Mark that image NSFW before you post it.", "그 이미지는 올리기 전에 부적절 콘텐츠 표시를 해."),
    "OMG": ("OMG, your hair looks amazing.", "세상에, 네 머리 정말 잘 어울린다."),
    "OML": ("OML, that scared me.", "맙소사, 그거 나 진짜 놀라게 했어."),
    "OMW": ("I'm OMW, save me a seat.", "가는 중이야. 자리 하나 맡아 줘."),
    "ONG": ("ONG, I didn't touch your phone.", "맹세코 나 네 휴대폰 안 만졌어."),
    "On fleek": ("Her eyeliner is on fleek.", "그녀의 아이라이너가 완벽해."),
    "On point": ("Your timing was on point.", "네 타이밍이 딱 맞았어."),
    "Only in Ohio": ("A vending machine selling soup? Only in Ohio.", "수프 파는 자판기라고? 진짜 이상한 상황이네."),
    "OTP": ("Those two characters are my OTP.", "그 두 캐릭터가 내가 제일 좋아하는 커플 조합이야."),
    "Periodt": ("I said what I said, periodt.", "난 할 말 했어, 더 말할 것도 없어."),
    "Pressed": ("Why are you pressed over one comment?", "댓글 하나 때문에 왜 그렇게 예민해?"),
    "Pulling": ("He's been pulling ever since he changed his haircut.", "머리 스타일 바꾼 뒤로 그는 인기를 끌고 있어."),
    "Put on blast": ("She put the company on blast for ignoring complaints.", "그녀는 불만을 무시한 회사를 공개적으로 비판했어."),
    "Rad": ("That old arcade is rad.", "그 오래된 오락실 진짜 멋져."),
    "Real": ("Be real, would you actually wear that?", "솔직히 말해 봐. 너 진짜 그거 입을 거야?"),
    "Receipts": ("If you're going to accuse her, bring receipts.", "그녀를 비난하려면 증거를 가져와."),
    "Rent free": ("That awkward moment lives rent free in my head.", "그 어색했던 순간이 아직도 머릿속에서 떠나질 않아."),
    "Rizz": ("He has zero rizz but somehow everyone likes him.", "그는 플러팅 실력은 전혀 없는데 이상하게 모두가 좋아해."),
    "RN": ("I can't talk rn.", "나 지금은 얘기 못 해."),
    "Salty": ("She's still salty about losing the bet.", "그녀는 내기에서 진 게 아직도 억울한가 봐."),
    "Savage": ("That comeback was savage.", "그 받아치기는 정말 세다."),
    "Say less": ("You want tacos after work? Say less.", "퇴근 후에 타코 먹자고? 더 말 안 해도 돼."),
    "Sending me": ("Your typo is sending me.", "네 오타 때문에 너무 웃겨."),
    "Shade": ("That was not advice; that was shade.", "그건 조언이 아니라 은근한 비꼼이었어."),
    "Ship": ("Fans ship them because their chemistry is obvious.", "팬들은 둘의 케미가 뚜렷해서 둘을 응원해."),
    "Shook": ("I was shook when I saw the final score.", "최종 점수를 보고 정말 놀랐어."),
    "Shorty": ("He called her shorty, and she rolled her eyes.", "그가 그녀를 쇼티라고 부르자 그녀는 눈을 굴렸어."),
    "Sick": ("That skateboard trick was sick.", "그 스케이트보드 기술 진짜 멋졌어."),
    "Simp": ("Buying flowers is sweet; texting 40 times is simp behavior.", "꽃을 사는 건 다정하지만 문자 40통은 너무 매달리는 행동이야."),
    "Skibidi Toilet": ("My little cousin keeps quoting Skibidi Toilet.", "내 어린 사촌이 계속 스키비디 토일럿을 따라 해."),
    "Slap": ("This bass line slaps.", "이 베이스 라인 진짜 좋다."),
    "Slay": ("You slayed that interview.", "너 그 면접 정말 잘 봤어."),
    "SMH": ("He forgot his passport at home. SMH.", "그는 여권을 집에 두고 왔어. 어이가 없네."),
    "S/O / SO": ("S/O to everyone who helped finish the project.", "프로젝트 마무리를 도와준 모두에게 감사 인사를 전해."),
    "Stan": ("I stan that singer's live vocals.", "난 그 가수의 라이브 실력을 정말 좋아해."),
    "Stoked": ("I'm stoked about the new job.", "새 직장 때문에 정말 신나."),
    "Sus": ("That discount link looks sus.", "그 할인 링크 좀 수상해 보여."),
    "Swerve": ("I had to swerve that awkward conversation.", "그 어색한 대화를 일부러 피해야 했어."),
    "Swole": ("He's been lifting for months and looks swole.", "그는 몇 달 동안 운동해서 몸이 탄탄해 보여."),
    "Swoop": ("Can you swoop me after practice?", "연습 끝나고 나 좀 데리러 와 줄래?"),
    "Take a seat": ("You clearly don't know the facts, so take a seat.", "너는 사실을 잘 모르는 것 같으니 그만 말해."),
    "Tea": ("What's the tea with those two?", "저 둘 사이에 무슨 소문 있어?"),
    "TFW": ("TFW you find money in an old jacket.", "오래된 재킷에서 돈을 찾았을 때 그 기분."),
    "Thirsty": ("Commenting on every selfie makes him look thirsty.", "셀카마다 댓글을 다는 건 그가 너무 관심을 바라는 것처럼 보여."),
    "Thirst Trap": ("She deleted the thirst trap before her aunt saw it.", "그녀는 이모가 보기 전에 그 도발적인 게시물을 지웠어."),
    "Touch grass": ("Log off and touch grass for an hour.", "한 시간만 로그아웃하고 현실로 좀 나와."),
    "Twin": ("We ordered the same drink again. Twin!", "우리 또 같은 음료 시켰네. 완전 통했어!"),
    "Twizzy": ("What's good, twizzy?", "잘 지내, 친구?"),
    "Unc": ("He called me unc because I didn't know the meme.", "내가 그 밈을 몰랐더니 그가 나를 아재라고 불렀어."),
    "Understood the assignment": ("The designer understood the assignment with that logo.", "디자이너가 그 로고를 정말 기대 이상으로 잘 만들었어."),
    "V": ("This is v important.", "이거 정말 중요해."),
    "Vanilla": ("The first draft felt too vanilla.", "첫 초안은 너무 평범하게 느껴졌어."),
    "Vibe": ("This room has a calm vibe.", "이 방은 차분한 분위기가 있어."),
    "VSCO girl": ("That bracelet stack is giving VSCO girl.", "그 팔찌 조합은 비스코 걸 느낌이 나."),
    "W": ("Getting home before the rain was a W.", "비 오기 전에 집에 온 건 성공이었어."),
    "Wallflower": ("I'm a wallflower at big parties.", "나는 큰 파티에서는 조용히 있는 편이야."),
    "Whip": ("He washed his whip before the road trip.", "그는 장거리 여행 전에 차를 세차했어."),
    "Woke": ("The term woke can be praise or criticism depending on tone.", "woke라는 말은 어조에 따라 칭찬일 수도 비판일 수도 있어."),
    "WYA": ("WYA? The movie starts in ten minutes.", "어디야? 영화 10분 뒤에 시작해."),
    "Yeet": ("Please don't yeet your backpack onto the couch.", "가방을 소파에 확 던지지 마."),
    "Zaddy": ("That actor has become the internet's favorite zaddy.", "그 배우는 인터넷에서 인기 있는 세련된 중년 남성이 됐어."),
}

ORIGINAL_EXAMPLE_KO = {
    "Addy": "거기서 만날게. 주소만 보내 줘.",
    "Amirite": "그 타코 진짜 맛있었지, 맞지?",
    "Amped": "오늘 밤 콘서트 때문에 완전 신났어!",
    "Aura": "어젯밤 스테프 커리의 결정적인 슛 봤어? 진짜 엄청난 존재감이 있어.",
    "Bae": "잠깐, 애인이 전화하고 있어.",
    "Bandwagon": "매기가 갑자기 럭비를 좋아하네. 완전 유행 따라 팬 된 거야.",
    "Basic": "그녀는 펌킨 스파이스 라테 마시는 게 너무 흔한 스타일이야.",
    "Bed rot": "정신없는 한 주를 보내고 나서 이번 주말에는 침대에서 푹 쉬고 싶어.",
    "Bet": "1: 우리 집에 올래? 2: 좋아!",
    "Boomer / Okay Boomer": "클레이턴의 큰삼촌이 밀레니얼 세대의 직업 윤리를 불평하기 시작하자, 그는 '오케이, 부머'라고 받아쳤어.",
    "Boujee": "너 이 고급 컨트리클럽에 가려는 건 아니지?",
    "Bussin'": "이 부리토 진짜 맛있다! 나 여기 꼭 다시 올 거야.",
    "Cap": "나 오늘 진짜 수업 갔어. 거짓말 아니야.",
    "Cash": "그 새 영화 진짜 멋져!",
    "Catch feels": "리아가 브루스에게 마음이 생기기 시작한 걸 알아챘어.",
    "Caught in 4k": "그는 거짓말하고도 넘어갈 수 있다고 생각했지만, 우리는 확실한 증거를 잡았어.",
    "Chat": "얘들아, 그가 진실을 말하는 것 같아?",
    "Cheugy": "그녀가 아직도 스키니진을 입는다니 믿기지 않아. 진짜 촌스럽다.",
    "Cooked": "밤새웠는데도 학습 가이드를 절반도 못 끝냈어. 나 망했어.",
    "Cringe": "애니가 제임스에게 말 걸려고 하는 걸 보는 건 너무 민망했어.",
    "Dank": "어젯밤 파티 진짜 좋았어!",
    "Dip": "나 이제 가려던 참이야.",
    "DL": "우리는 대화 중이지만 지금은 비밀로 하고 있어.",
    "Dope": "그 자전거 진짜 멋지다!",
    "Dox": "제니퍼는 온라인 게임에서 누군가와 싸운 뒤 개인정보가 공개됐어. 이제 그녀의 주소와 전화번호가 소셜 미디어에 퍼졌어.",
    "Drag": "베티는 피터를 조롱한 뒤로 다시는 초대받지 못할 거야.",
    "Drip": "너 그 새 신발 신고 스타일 진짜 좋다.",
    "Dub": "우리가 승리했어.",
    "Egirl / Eboy": "내 스타일을 이보이 같은 느낌으로 바꿔 볼까 생각 중이야.",
    "Extra": "난 그녀를 초대하지 않았어. 너무 과하게 행동하거든.",
    "Facts": "1: 그의 새 앨범 진짜 좋다. 2: 완전 인정!",
    "Faded": "어젯밤 그녀를 봤어야 했어. 완전 취해 있었어.",
    "Fan service": "마블 팬이라면 이번 에피소드를 좋아할 거야. 팬서비스가 정말 많거든.",
    "Finna": "나 쇼핑몰에 갈 거야.",
    "Finsta": "그녀는 친한 친구들이 보도록 비공개 계정에 웃긴 셀카와 비하인드 장면을 올렸어.",
    "Fire": "저 워터슬라이드 진짜 대박이야!",
    "Fit": "너는 항상 패셔너블해. 착장 정말 멋지다!",
    "Flex": "그는 그 운동화를 신고 자랑하고 있어.",
    "FR": "1: 숙제 진짜 어려웠어. 2: 인정.",
    "FRFR": "너 기다리는 거 지쳤어. 쇼핑몰은 언제나 똑같잖아. 진짜로!",
    "FYP": "오늘 내 추천 피드에 진짜 이상한 것들이 떴어.",
    "Gassing": "그녀는 이미 충분히 자신감 있어. 더 띄워 줄 필요 없어.",
    "Ghost": "우리는 데이트를 했고, 그 뒤로 그는 연락을 끊었어.",
    "Giving me life": "이 따뜻한 날씨가 나를 살맛 나게 해!",
    "Glow-up": "그녀는 확 달라졌어. 정말 좋아 보인다!",
    "GOAT": "내 코치는 역대 최고야!",
    "Granola": "아마 산책로나 등산길에서 그녀를 만날 거야. 그녀는 자연친화적인 사람이거든.",
    "Guap": "샐리는 그 신발에 돈을 엄청 많이 냈을 거야.",
    "Gucci": "1: 10분 뒤에 데리러 갈게. 2: 좋아.",
    "Hammered": "그는 너무 취해서 우리가 응급실에 데려가야 했어.",
    "Heated": "내가 그의 계산서를 가져갔다고 말하자 그는 화가 났어.",
    "Here for this": "너 완전 보스처럼 변하고 있네. 난 이거 좋아.",
    "High key": "나 그 새 영화 진짜 좋아해.",
    "Hits different": "엄마가 해 주는 음식은 유난히 특별하게 느껴져.",
    "Hollywood": "앨리스는 치어리딩 팀에 들어간 뒤 거만하게 변했어.",
    "Hop off": "그가 계속 질문하며 그녀를 귀찮게 하자, 그녀는 그만하고 공간 좀 달라고 했어.",
    "Hot take": "새 슈퍼히어로 영화를 봤어. 출연진은 훌륭했지만 줄거리는 좀 별로였어. 이게 오늘 내 과감한 의견이야.",
    "Hype": "이 노래 진짜 신난다!",
    "Ick": "그가 어린 동생에게 얼마나 못되게 굴었는지 봤어? 그거 진짜 정떨어져.",
    "ICYMI": "혹시 못 봤다면, 나 이번 가을에 아이유 스테이트로 가.",
    "IRL": "그는 온라인 친구가 많지만 실제로 만난 적은 없어.",
    "IYKYK": "그 스키 여행 진짜 난리였어! 아는 사람은 알지.",
    "Juul": "그녀는 버스를 기다리면서 몰래 전자담배를 꺼내 한 모금 피웠어.",
    "Keep it 100": "친구들이 진실이 듣기 힘들더라도 나에게 솔직하게 말해 줄 때 고마워.",
    "L": "그는 패배했어.",
    "Left on read": "어젯밤 그에게 문자를 보냈는데 읽고 답이 없었어. 바쁜 건지 그냥 무시하는 건지 모르겠어.",
    "Lit": "그 영화 진짜 재밌었어!",
    "LMAO": "내가 계단을 올라가다가 넘어진 거 기억나? 완전 웃겨!",
    "LMS": "경품 행사에 참여하려면 내 상태 글에 좋아요 눌러.",
    "LOL": "네 타조 영상 보고 웃었어!",
    "Mad": "밖이 진짜 엄청 더워.",
    "Mid": "그 쇼는 그냥 그저 그랬어.",
    "Netflix and chill": "리키에게 넷플릭스 보고 쉬자고 했더니, 그는 진짜 팝콘을 들고 왔어. 하하.",
    "NGL": "많은 사람들이 그 영화를 안 좋아했지만, 솔직히 난 좋았어.",
    "NSFW": "지금 그 링크는 못 열어. 부적절 콘텐츠로 표시되어 있고 나는 학교에 있어.",
    "OMG": "세상에, 네가 방금 그렇게 말했다니 믿기지 않아!",
    "OML": "맙소사, 너 때문에 깜짝 놀랐어!",
    "OMW": "가는 중이야! 20분 안에 도착할게.",
    "ONG": "방금 그들이 키스하는 걸 봤어! 맹세코 진짜야.",
    "On fleek": "네 메이크업 완벽하다.",
    "On point": "그의 옷차림은 딱 좋아.",
    "Only in Ohio": "왜 기차에 쥐가 있어? 진짜 이상한 상황이네.",
    "OTP": "난 파일럿 에피소드 때부터 이 커플 조합을 응원했어. 둘의 케미가 화면에서 최고야.",
    "Periodt": "그는 그 그룹에서 최고의 댄서야, 더 말할 것도 없어.",
    "Pressed": "왜 그렇게 예민해?",
    "Pulling": "그가 파티에서 적어도 여자 다섯 명의 관심을 끄는 걸 봤어.",
    "Put on blast": "그는 문자로 그녀와 헤어진 일 때문에 공개적으로 비난받았어.",
    "Rad": "이 전망 정말 멋지다.",
    "Real": "네가 그 드레스를 소화할 수 있다고 생각해? 현실적으로 생각해 봐.",
    "Receipts": "그녀가 내가 거짓말한다고 하자, 그는 대화 캡처를 증거로 준비해 와서 자기 주장을 증명했어.",
    "Rent free": "그가 나에게 한 말이 아직도 내 머릿속에서 떠나지 않아.",
    "Rizz": "그 남자애는 매력이 엄청나. 초등학교 이후로 어떻게 계속 싱글이었지?",
    "RN": "나 지금 바빠. 나중에 전화할게.",
    "Salty": "그는 진 뒤에 삐쳐 있어서 내가 게임에서 나가라고 했어.",
    "Savage": "그는 코트에서 정말 거침없어.",
    "Say less": "그녀가 둘이 좋아하는 식당에 가자고 하자, 그는 고개를 끄덕이며 '알겠어'라고만 했어.",
    "Sending me": "ㅋㅋㅋ 그 판다 밈 진짜 너무 웃겨!",
    "Shade": "그녀 방금 나를 은근히 비꼰 거야?",
    "Ship": "난 티모시 샬라메와 카일리 제너 커플을 완전 응원해.",
    "Shook": "그녀가 진짜 과제를 했어. 나 완전 놀랐어!",
    "Shorty": "안녕, 예쁜이! 한잔하러 가자.",
    "Sick": "그 태클 봤어? 진짜 멋졌어!",
    "Simp": "야, 너 너무 매달리는 것처럼 굴고 있어.",
    "Skibidi Toilet": "사람들은 캐주얼한 온라인 대화에서 '스키비디 토일럿'을 언급하곤 해.",
    "Slap": "이 노래 진짜 좋다!",
    "Slay": "너 댄스 발표회 정말 잘했어!",
    "SMH": "제인에게 비행기 타기 전에 샤워할 시간이 부족하다고 경고했어. 내가 맞았고, 그는 비행기를 놓쳤어. 어이가 없네.",
    "S/O / SO": "이 사진을 찍어 준 소피에게 감사 인사를 전해.",
    "Stan": "예전에는 그를 엄청 좋아했지만, 이제는 아니야.",
    "Stoked": "그가 나를 초대했을 때 정말 신났어.",
    "Sus": "너 거짓말하는 거야, 아니면 뭐야? 요즘 행동이 정말 수상해.",
    "Swerve": "전 애인을 봤을 때 일부러 피했어.",
    "Swole": "올해 내 목표는 근육을 정말 키우는 거야.",
    "Swoop": "네 차가 정비소에 있으니까, 내가 10분 뒤에 데리러 갈게.",
    "Take a seat": "그 사람이 통제 불능으로 굴어서 내가 '진정하고 그만해'라고 말했어.",
    "Tea": "사라는 그 일에 대해 알 거야. 그냥 물어봐. 그녀는 소문 얘기하는 걸 좋아해.",
    "TFW": "눈 내리는 바깥을 보며 핫초코를 들고 아늑하게 있을 때의 그 기분.",
    "Thirsty": "그는 내 인스타그램을 팔로우하자마자 내 모든 게시물에 좋아요를 눌렀어. 관심을 너무 갈구하는 것 같아.",
    "Thirst Trap": "그가 틱톡에 올리는 건 전부 관심 끌려는 도발적인 게시물이야.",
    "Touch grass": "주말 내내 비디오게임을 한 뒤, 친구들이 이제 현실로 나와 햇빛 좀 쐬라고 했어.",
    "Twin": "친구야, 언제 놀러 올 거야?",
    "Twizzy": "친구야, 언제 놀러 올 거야?",
    "Unc": "계단을 올라가기만 했는데 너무 피곤해서, 내가 이제 아재가 된 것 같아.",
    "Understood the assignment": "이번 생일은 최고였어! 너 정말 기대 이상으로 해냈어.",
    "V": "나 다음 주말 프롬 때문에 정말 신나.",
    "Vanilla": "그와 대화를 해 보려고 했지만, 그는 너무 평범하고 재미없어.",
    "Vibe": "네 전체적인 분위기가 정말 좋아.",
    "VSCO girl": "그녀는 큰 티셔츠와 버켄스탁을 신고, 커다란 하이드로 플라스크를 들고 있어. 완전 비스코 걸처럼 보이려는 것 같아.",
    "W": "우리 팀이 승리했어.",
    "Wallflower": "그녀는 학교 댄스파티에서 늘 조용히 있는 편이었어.",
    "Whip": "그녀가 새 차를 타고 막 도착했어.",
    "Woke": "예전에는 주변에서 무슨 일이 일어나는지 잘 몰랐지만, 이제는 사회 문제에 깨어 있어.",
    "WYA": "어디 있는지 알려 줘. 내가 만나러 갈게.",
    "Yeet": "그가 땅콩버터 병을 창밖으로 확 던졌어.",
    "Zaddy": "그녀는 졸업하자마자 멋진 연상 남자를 만났어.",
}


CORRECTIONS = {
    "Bussin’": "Bussin'",
    "SO": "S/O / SO",
}

NOTES = {
    "Cash": "원문 뜻은 유지했지만, 현재 일상 슬랭으로는 다소 오래되거나 지역성이 있습니다.",
    "Faded": "약물 또는 취한 상태와 관련된 표현입니다.",
    "Finna": "AAVE에서 온 표현이라 가볍게 흉내 내듯 쓰면 부자연스럽거나 무례할 수 있습니다.",
    "Hammered": "술 또는 약물에 많이 취한 상태를 뜻합니다.",
    "Juul": "전자담배 브랜드명입니다.",
    "Netflix and chill": "성적 뉘앙스가 있는 완곡 표현입니다.",
    "On fleek": "의미는 맞지만 최근에는 약간 예전 유행처럼 들릴 수 있습니다.",
    "S/O / SO": "shout out은 보통 S/O로, significant other는 SO로 쓰입니다. 원문 표기를 보정했습니다.",
    "Shorty": "친하지 않은 상대에게 쓰면 무례하거나 대상화하는 말로 들릴 수 있습니다.",
    "Skibidi Toilet": "일반 단어형 슬랭이라기보다 인터넷 밈/콘텐츠명입니다.",
    "Thirst Trap": "성적 뉘앙스가 있는 소셜 미디어 표현입니다.",
    "Woke": "문맥에 따라 긍정 또는 비꼼으로 갈립니다.",
}

LETTER_PRONUNCIATION = {
    "A": "에이",
    "B": "비",
    "C": "씨",
    "D": "디",
    "E": "이",
    "F": "에프",
    "G": "지",
    "H": "에이치",
    "I": "아이",
    "J": "제이",
    "K": "케이",
    "L": "엘",
    "M": "엠",
    "N": "엔",
    "O": "오",
    "P": "피",
    "Q": "큐",
    "R": "알",
    "S": "에스",
    "T": "티",
    "U": "유",
    "V": "브이",
    "W": "더블유",
    "X": "엑스",
    "Y": "와이",
    "Z": "지",
}

WORD_PRONUNCIATION = {
    "about": "어바웃",
    "account": "어카운트",
    "adult": "어덜트",
    "all": "올",
    "amazing": "어메이징",
    "are": "아",
    "at": "앳",
    "atmosphere": "애트머스피어",
    "average": "애버리지",
    "avoid": "어보이드",
    "awesome": "어썸",
    "back": "백",
    "baddie": "배디",
    "be": "비",
    "best": "베스트",
    "bestie": "베스티",
    "better": "베터",
    "big": "빅",
    "bit": "빗",
    "bold": "볼드",
    "boo": "부",
    "brag": "브래그",
    "bring": "브링",
    "buff": "버프",
    "busted": "버스티드",
    "calm": "캄",
    "call": "콜",
    "car": "카",
    "cash": "캐시",
    "charisma": "커리즈마",
    "charm": "참",
    "close": "클로스",
    "content": "콘텐츠",
    "cool": "쿨",
    "couple": "커플",
    "crush": "크러시",
    "crushed": "크러시트",
    "cursed": "커스트",
    "dead": "데드",
    "defeat": "디피트",
    "delicious": "딜리셔스",
    "delivered": "딜리버드",
    "dig": "딕",
    "dodge": "다지",
    "done": "던",
    "drama": "드라마",
    "drunk": "드렁크",
    "duck": "덕",
    "easter": "이스터",
    "egg": "에그",
    "energy": "에너지",
    "everyone": "에브리원",
    "evidence": "에비던스",
    "excellent": "엑설런트",
    "excited": "익사이티드",
    "explicit": "익스플리싯",
    "expose": "익스포즈",
    "facepalm": "페이스팜",
    "fail": "페일",
    "favorite": "페이버릿",
    "fine": "파인",
    "fire": "파이어",
    "flawless": "플로리스",
    "flaunt": "플론트",
    "for": "포",
    "friend": "프렌드",
    "game": "게임",
    "get": "겟",
    "girl": "걸",
    "give": "기브",
    "gonna": "거너",
    "good": "굿",
    "gossip": "가십",
    "great": "그레이트",
    "guys": "가이즈",
    "haha": "하하",
    "headed": "헤디드",
    "high": "하이",
    "hit": "힛",
    "honest": "아니스트",
    "honestly": "아니슬리",
    "hook": "훅",
    "hurl": "헐",
    "hyped": "하이프트",
    "ignore": "이그노어",
    "in": "인",
    "inappropriate": "이너프로프리엇",
    "inside": "인사이드",
    "intoxicated": "인톡시케이티드",
    "jacked": "잭트",
    "joke": "조크",
    "launch": "론치",
    "leave": "리브",
    "legend": "레전드",
    "lie": "라이",
    "like": "라이크",
    "location": "로케이션",
    "loss": "로스",
    "meme": "밈",
    "money": "머니",
    "mood": "무드",
    "muscular": "머스큘러",
    "nail": "네일",
    "nailed": "네일드",
    "needy": "니디",
    "no": "노",
    "nod": "나드",
    "not": "낫",
    "observer": "옵저버",
    "offline": "오프라인",
    "okay": "오케이",
    "old": "올드",
    "one": "원",
    "online": "온라인",
    "outside": "아웃사이드",
    "pairing": "페어링",
    "perfect": "퍼펙트",
    "plain": "플레인",
    "politically": "폴리티컬리",
    "post": "포스트",
    "praise": "프레이즈",
    "private": "프라이빗",
    "proof": "프루프",
    "rad": "래드",
    "real": "리얼",
    "really": "리얼리",
    "ride": "라이드",
    "right": "라이트",
    "rofl": "로플",
    "root": "루트",
    "say": "세이",
    "screenshots": "스크린샷츠",
    "serious": "시리어스",
    "seriously": "시리어슬리",
    "shady": "셰이디",
    "shame": "셰임",
    "shout": "샤웃",
    "sick": "식",
    "significant": "시그니피컨트",
    "similar": "시밀러",
    "sit": "싯",
    "sketchy": "스케치",
    "socially": "소셜리",
    "spot": "스팟",
    "stack": "스택",
    "status": "스테이터스",
    "stop": "스탑",
    "stream": "스트림",
    "super": "수퍼",
    "sure": "슈어",
    "suspicious": "서스피셔스",
    "swag": "스웨그",
    "that": "댓",
    "there": "데어",
    "throw": "스로우",
    "to": "투",
    "toast": "토스트",
    "top": "탑",
    "trend": "트렌드",
    "true": "트루",
    "uncle": "엉클",
    "under": "언더",
    "up": "업",
    "vehicle": "비이클",
    "very": "베리",
    "victory": "빅터리",
    "vibe": "바이브",
    "vape": "베이프",
    "weird": "위어드",
    "where": "웨어",
    "win": "윈",
    "you": "유",
}


def parse_markdown(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    parts = re.split(r"^###\s+", text, flags=re.MULTILINE)[1:]
    entries = []
    for part in parts:
        lines = part.splitlines()
        original_term = lines[0].strip()
        if not original_term or original_term.startswith("_"):
            continue
        term = CORRECTIONS.get(original_term, original_term)
        body = "\n".join(lines[1:])
        meaning_match = re.search(
            r"\*\*Meaning:\*\*\s*(.*?)(?:\n\*\*Example:\*\*|\Z)",
            body,
            flags=re.DOTALL,
        )
        example_match = re.search(
            r"\*\*Example:\*\*\s*(.*?)(?:\n##\s|\Z)",
            body,
            flags=re.DOTALL,
        )
        meaning = clean_inline(meaning_match.group(1)) if meaning_match else ""
        example = clean_inline(example_match.group(1)) if example_match else ""
        if not meaning:
            continue
        entries.append(
            {
                "term": term,
                "original_term": original_term,
                "meaning_en": meaning,
                "pronunciation_ko": PRONUNCIATION.get(term, ""),
                "explanation_ko": KO.get(term, ""),
                "examples": build_examples(term, example),
                "similar": build_similar(term),
                "note": NOTES.get(term, ""),
            }
        )
    return entries


def clean_inline(value: str) -> str:
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"  \n", "\n", value)
    value = re.sub(r"\s*\n\s*", " ", value)
    value = value.replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", value).strip()


def build_examples(term: str, source_example: str) -> list[dict]:
    source = source_example or f"People use '{term}' in casual online conversations."
    source_ko = ORIGINAL_EXAMPLE_KO.get(term, "")
    added_en, added_ko = ADDED_EXAMPLES.get(
        term,
        (
            f"People use '{term}' in casual online conversations.",
            "이 표현은 주로 캐주얼한 온라인 대화에서 쓰입니다.",
        ),
    )
    return [
        {"en": source, "ko": source_ko},
        {"en": added_en, "ko": added_ko},
    ]


def build_similar(term: str) -> list[dict]:
    related = []
    for text in SIMILAR.get(term, []):
        related.append(
            {
                "en": text,
                "pronunciation_ko": pronounce_related(text),
                "explanation_ko": f"'{term}'와 의미나 쓰임이 가까운 대체 표현입니다.",
                "example": {
                    "en": make_related_example(text),
                    "ko": "비슷한 맥락에서 함께 익혀 두면 좋은 표현입니다.",
                },
            }
        )
    return related


def pronounce_related(text: str) -> str:
    stripped = re.sub(r"[^A-Za-z0-9 ]", "", text).strip()
    if stripped and stripped.replace(" ", "").isupper():
        return " ".join(LETTER_PRONUNCIATION.get(ch, ch) for ch in stripped if ch != " ")

    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    if not words:
        return text
    parts = []
    for word in words:
        if word.isdigit():
            parts.append(word)
        elif word in WORD_PRONUNCIATION:
            parts.append(WORD_PRONUNCIATION.get(word, word))
        else:
            return ""
    return " ".join(parts) if parts else ""


def make_related_example(text: str) -> str:
    clean = text.strip()
    return f"You may hear '{clean}' in a similar casual context."


def render_html(entries: list[dict]) -> str:
    data = json.dumps(entries, ensure_ascii=False).replace("</", "<\\/")
    generated = date.today().isoformat()
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slang Glossary</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f5f7fb; color: #172033; }}
    header {{ background: #152238; color: #fff; padding: 24px 18px 18px; }}
    .wrap {{ max-width: 1040px; margin: 0 auto; }}
    h1 {{ margin: 0; font-size: 28px; letter-spacing: 0; }}
    .sub {{ margin: 8px 0 0; color: #c9d6e8; font-size: 14px; }}
    .toolbar {{ position: sticky; top: 0; z-index: 2; background: rgba(245,247,251,.96); border-bottom: 1px solid #d9e2ef; padding: 12px 18px; backdrop-filter: blur(8px); }}
    .toolbar-inner {{ max-width: 1040px; margin: 0 auto; display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center; }}
    .alpha-nav {{ max-width: 1040px; margin: 10px auto 0; display: flex; flex-wrap: wrap; gap: 5px; }}
    .alpha-btn {{ border: 1px solid #c8d3e2; background: #fff; color: #30415d; border-radius: 6px; min-width: 32px; height: 32px; padding: 0 8px; font-weight: 700; cursor: pointer; }}
    .alpha-btn:hover {{ background: #eef4ff; border-color: #2f6fbd; }}
    .alpha-btn.active {{ background: #2f6fbd; border-color: #2f6fbd; color: #fff; }}
    .alpha-btn:disabled {{ opacity: .35; cursor: default; background: #f3f6fb; }}
    input {{ width: 100%; height: 42px; border: 1px solid #c8d3e2; border-radius: 8px; padding: 0 12px; font-size: 15px; background: #fff; }}
    .count {{ color: #516178; font-size: 14px; white-space: nowrap; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 18px; }}
    .page-title {{ display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-bottom: 12px; color: #172033; }}
    .page-title h2 {{ font-size: 24px; }}
    .page-title span {{ color: #6b7890; font-size: 14px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; }}
    article {{ background: #fff; border: 1px solid #dce4ef; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(14, 31, 53, .04); }}
    .top {{ display: flex; justify-content: space-between; gap: 10px; align-items: start; }}
    .title-row {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
    h2 {{ margin: 0; font-size: 21px; color: #172033; letter-spacing: 0; }}
    .letter {{ display: inline-flex; min-width: 28px; height: 28px; border-radius: 6px; align-items: center; justify-content: center; background: #e9eef7; color: #30415d; font-weight: 700; font-size: 13px; }}
    .pron {{ margin-top: 4px; color: #6b7890; font-size: 13px; }}
    .meaning {{ margin-top: 12px; font-size: 14px; color: #34445c; }}
    .ko {{ margin-top: 10px; padding: 10px; border-radius: 6px; background: #f7fafc; color: #24344d; font-size: 14px; line-height: 1.58; }}
    .label {{ margin-top: 13px; font-size: 12px; font-weight: 700; color: #2f6fbd; text-transform: uppercase; }}
    .example {{ margin-top: 6px; font-size: 13px; color: #26344b; line-height: 1.5; }}
    .line {{ display: flex; align-items: flex-start; gap: 6px; }}
    .line-text {{ min-width: 0; }}
    .example span {{ display: block; color: #748196; margin-top: 2px; }}
    .related {{ display: grid; gap: 8px; margin-top: 8px; }}
    .related-item {{ border: 1px solid #e3eaf4; border-radius: 8px; padding: 10px; background: #fbfdff; }}
    .related-head {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; font-size: 13px; }}
    .related-head strong {{ color: #172033; }}
    .related-pron {{ color: #6b7890; }}
    .related-desc {{ margin-top: 5px; color: #4a5870; font-size: 12px; line-height: 1.45; }}
    .related-example {{ margin-top: 5px; color: #26344b; font-size: 12px; line-height: 1.45; }}
    .related-example span {{ display: block; color: #748196; }}
    .note {{ margin-top: 12px; border-top: 1px dashed #d9e2ef; padding-top: 10px; color: #8a4b12; font-size: 13px; line-height: 1.5; }}
    .note strong {{ color: #7a3f08; }}
    .speak {{ flex: 0 0 auto; border: 1px solid #c8d3e2; background: #fff; color: #2f6fbd; border-radius: 999px; width: 28px; height: 28px; cursor: pointer; font-size: 13px; line-height: 1; display: inline-flex; align-items: center; justify-content: center; }}
    .speak:hover {{ background: #eef4ff; border-color: #2f6fbd; }}
    .speak.playing {{ background: #2f6fbd; color: #fff; border-color: #2f6fbd; }}
    mark {{ background: #fff0a6; padding: 0 2px; }}
    @media (max-width: 640px) {{
      h1 {{ font-size: 23px; }}
      .toolbar-inner {{ grid-template-columns: 1fr; }}
      main {{ padding: 12px; }}
      .grid {{ grid-template-columns: 1fr; }}
      .alpha-nav {{ overflow-x: auto; flex-wrap: nowrap; padding-bottom: 2px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Slang Glossary</h1>
      <p class="sub">PDF handout 기반 · 한국어 설명, 발음, 예문, 유사 표현, TTS 보강 · {generated}</p>
    </div>
  </header>
  <div class="toolbar">
    <div class="toolbar-inner">
      <input id="search" type="search" placeholder="표현, 뜻, 한국어 설명으로 검색">
      <div class="count" id="count"></div>
    </div>
    <nav class="alpha-nav" id="alpha-nav" aria-label="알파벳 인덱스"></nav>
  </div>
  <main>
    <div class="page-title">
      <h2 id="page-letter"></h2>
      <span id="page-range"></span>
    </div>
    <section class="grid" id="grid"></section>
  </main>
  <script id="slang-data" type="application/json">{data}</script>
  <script>
    const entries = JSON.parse(document.getElementById('slang-data').textContent);
    const grid = document.getElementById('grid');
    const search = document.getElementById('search');
    const count = document.getElementById('count');
    const alphaNav = document.getElementById('alpha-nav');
    const pageLetter = document.getElementById('page-letter');
    const pageRange = document.getElementById('page-range');
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    let activeLetter = new URLSearchParams(location.search).get('letter') || location.hash.replace('#', '') || entries[0].term[0].toUpperCase();

    function esc(value) {{
      return String(value || '').replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
    }}

    function render(list) {{
      const letterItems = entries.filter(item => item.term[0].toUpperCase() === activeLetter);
      const first = letterItems[0]?.term || '';
      const last = letterItems[letterItems.length - 1]?.term || '';
      pageLetter.textContent = `${{activeLetter}}`;
      pageRange.textContent = first && last ? `${{first}} - ${{last}}` : '항목 없음';
      count.textContent = `${{list.length}} / ${{letterItems.length}}`;
      grid.innerHTML = list.map(item => `
        <article>
          <div class="top">
            <div>
              <div class="title-row">
                <h2>${{esc(item.term)}}</h2>
                <button class="speak" data-speak="${{esc(item.term)}}" title="표현 발음 듣기" aria-label="표현 발음 듣기">🔊</button>
              </div>
              <div class="pron">${{esc(item.pronunciation_ko)}}</div>
            </div>
            <div class="letter">${{esc(item.term[0].toUpperCase())}}</div>
          </div>
          <div class="meaning"><strong>원뜻:</strong> ${{esc(item.meaning_en)}}</div>
          <div class="ko">${{esc(item.explanation_ko)}}</div>
          <div class="label">Examples</div>
          ${{item.examples.map(ex => `
            <div class="example">
              <div class="line">
                <button class="speak" data-speak="${{esc(ex.en)}}" title="예문 발음 듣기" aria-label="예문 발음 듣기">🔊</button>
                <div class="line-text">"${{esc(ex.en)}}"<span>${{esc(ex.ko)}}</span></div>
              </div>
            </div>
          `).join('')}}
          <div class="label">Similar</div>
          <div class="related">
            ${{item.similar.map(s => `
              <div class="related-item">
                <div class="related-head">
                  <button class="speak" data-speak="${{esc(s.en)}}" title="유의어 발음 듣기" aria-label="유의어 발음 듣기">🔊</button>
                  <strong>${{esc(s.en)}}</strong>
                  ${{s.pronunciation_ko ? `<span class="related-pron">${{esc(s.pronunciation_ko)}}</span>` : ''}}
                </div>
                <div class="related-desc">${{esc(s.explanation_ko)}}</div>
                <div class="related-example">
                  <div class="line">
                    <button class="speak" data-speak="${{esc(s.example.en)}}" title="유의어 예문 발음 듣기" aria-label="유의어 예문 발음 듣기">🔊</button>
                    <div class="line-text">"${{esc(s.example.en)}}"<span>${{esc(s.example.ko)}}</span></div>
                  </div>
                </div>
              </div>
            `).join('')}}
          </div>
          ${{item.note ? `<div class="note"><strong>주의:</strong> ${{esc(item.note)}}</div>` : ''}}
        </article>
      `).join('');
    }}

    function filter() {{
      const q = search.value.trim().toLowerCase();
      const letterItems = entries.filter(item => item.term[0].toUpperCase() === activeLetter);
      if (!q) return render(letterItems);
      render(letterItems.filter(item => JSON.stringify(item).toLowerCase().includes(q)));
    }}

    function renderAlphaNav() {{
      const available = new Set(entries.map(item => item.term[0].toUpperCase()));
      if (!available.has(activeLetter)) activeLetter = [...available][0];
      alphaNav.innerHTML = alphabet.map(letter => `
        <button class="alpha-btn ${{letter === activeLetter ? 'active' : ''}}"
                data-letter="${{letter}}"
                ${{available.has(letter) ? '' : 'disabled'}}
                aria-current="${{letter === activeLetter ? 'page' : 'false'}}">${{letter}}</button>
      `).join('');
    }}

    alphaNav.addEventListener('click', event => {{
      const button = event.target.closest('[data-letter]');
      if (!button || button.disabled) return;
      activeLetter = button.dataset.letter;
      search.value = '';
      history.replaceState(null, '', `#${{activeLetter}}`);
      renderAlphaNav();
      filter();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }});

    search.addEventListener('input', filter);
    let currentButton = null;
    document.addEventListener('click', event => {{
      const button = event.target.closest('[data-speak]');
      if (!button || typeof speechSynthesis === 'undefined') return;
      const text = button.dataset.speak;
      if (!text) return;
      speechSynthesis.cancel();
      if (currentButton) currentButton.classList.remove('playing');
      button.classList.add('playing');
      currentButton = button;
      setTimeout(() => {{
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.onend = () => {{
          button.classList.remove('playing');
          currentButton = null;
        }};
        utterance.onerror = () => {{
          button.classList.remove('playing');
          currentButton = null;
        }};
        speechSynthesis.speak(utterance);
      }}, 50);
    }});
    renderAlphaNav();
    filter();
  </script>
</body>
</html>"""


def build():
    source_path = os.path.join(BASE_DIR, "slang_20260427_markdown.md")
    output_path = os.path.join(BASE_DIR, "docs", "slang.html")
    entries = parse_markdown(source_path)
    missing = [
        item["term"]
        for item in entries
        if not item["pronunciation_ko"] or not item["explanation_ko"] or not item["similar"]
    ]
    if missing:
        raise RuntimeError(f"Missing enrichment for: {', '.join(missing)}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(render_html(entries))
    print(f"Built {output_path} with {len(entries)} entries")


if __name__ == "__main__":
    build()
