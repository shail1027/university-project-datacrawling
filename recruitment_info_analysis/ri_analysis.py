import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

def analysis_recruit_info(titles):
    train_titles, test_titles = train_test_split(titles, test_size=0.3, random_state=0)

    train_titles = [normalize_title_1(t) for t in train_titles]
    test_titles  = [normalize_title_2(t) for t in test_titles]

    train_labels = []

    for title in train_titles:
        if "IT" in title or "시스템" in title:
            train_labels.append(0)
        elif "기획" in title or "마케팅" in title:
            train_labels.append(1)
        elif "금융" in title or "증권" in title:
            train_labels.append(2)
        elif "건설" in title or "시공" in title:
            train_labels.append(3)
        elif "디자인" in title or "편집" in title:
            train_labels.append(4)
        else:
            train_labels.append(5)

    test_labels = []

    for title in test_titles:
        if "개발" in title or "엔지니어" in title:
            test_labels.append(0)
        elif "콘텐츠" in title or "홍보" in title:
            test_labels.append(1)
        elif "투자" in title or "자산" in title:
            test_labels.append(2)
        elif "건축" in title or "설비" in title:
            test_labels.append(3)
        elif "디자이너" in title or "제작" in title:
            test_labels.append(4)
        else:
            test_labels.append(5)

    vectorizer = TfidfVectorizer(min_df=3, max_df=0.8)

    X_train = vectorizer.fit_transform(train_titles)
    X_test = vectorizer.transform(test_titles)

    lr_ri = LogisticRegression()
    lr_ri.fit(X_train, train_labels)

    Y_predict = lr_ri.predict(X_test)

    print("Confusion Matrix(오차 행렬)")
    print(confusion_matrix(test_labels, Y_predict))
    print("\nPrecision Score(정밀도):",
        precision_score(test_labels, Y_predict, average="macro", zero_division=0))
    print("Recall Score(재현율):",
        recall_score(test_labels, Y_predict, average="macro", zero_division=0))
    print("F1 Score(F1 스코어):",
        f1_score(test_labels, Y_predict, average="macro", zero_division=0))

def normalize_title_1(title):
    title = title.upper()

    # IT / 시스템 / 개발자
    for keyword in ["S/W", "SW", "SOFTWARE", "개발자", "개발", "ENGINEER", "엔지니어", "시스템"]:
        if keyword in title:
            title = title.replace(keyword, "IT")

    # 기획 / 마케팅
    for keyword in ["기획", "마케팅", "콘텐츠", "브랜드", "홍보"]:
        if keyword in title:
            title = title.replace(keyword, "기획")

    # 금융 / 증권
    for keyword in ["금융", "증권", "투자", "자산", "은행"]:
        if keyword in title:
            title = title.replace(keyword, "금융")

    # 건설 / 시공
    for keyword in ["건설", "시공", "토목", "현장"]:
        if keyword in title:
            title = title.replace(keyword, "건설")

    # 디자인 / 편집
    for keyword in ["디자인", "편집", "그래픽", "영상"]:
        if keyword in title:
            title = title.replace(keyword, "디자인")

    return title

def normalize_title_2(title):
    title = title.upper()

    # IT / 시스템 / 개발자
    for keyword in ["S/W", "SW", "SOFTWARE", "개발자", "개발", "ENGINEER", "엔지니어", "시스템"]:
        if keyword in title:
            title = title.replace(keyword, "개발")

    # 기획 / 마케팅
    for keyword in ["기획", "마케팅", "콘텐츠", "브랜드", "홍보"]:
        if keyword in title:
            title = title.replace(keyword, "콘텐츠")

    # 금융 / 증권
    for keyword in ["금융", "증권", "투자", "자산", "은행"]:
        if keyword in title:
            title = title.replace(keyword, "투자")

    # 건설 / 시공
    for keyword in ["건설", "시공", "토목", "현장"]:
        if keyword in title:
            title = title.replace(keyword, "건축")

    # 디자인 / 편집
    for keyword in ["디자인", "편집", "그래픽", "영상"]:
        if keyword in title:
            title = title.replace(keyword, "디자이너")

    return title

def analysis_skuniv_recruit_info():
    data = pd.read_csv("./skuniv_recruitment_titles.csv", encoding="utf-8-sig")
    #print(len(data))
    #print(data[:5])

    titles = data['title'].tolist()
    analysis_recruit_info(titles)

def analysis_jobkorea_recruit_info():
    data = pd.read_csv("./jobkorea_recruitment_titles.csv", encoding="utf-8-sig")

    titles = data['title'].tolist()
    analysis_recruit_info(titles)


print("\n========교내 채용 제목 분석============")
analysis_skuniv_recruit_info()

print("\n========잡코리아 채용 제목 분석============")
analysis_jobkorea_recruit_info()