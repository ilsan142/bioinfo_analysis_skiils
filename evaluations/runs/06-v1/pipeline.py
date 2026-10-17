from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# X에는 동일 환자의 두 번 방문 자료가 행으로 있다. y는 질병 label이다.
# X, y, patient_id는 호출 측에서 전달한다.
def evaluate(X, y, patient_id):
    selected = SelectKBest(f_classif, k=10).fit_transform(X, y)
    train_x, test_x, train_y, test_y = train_test_split(selected, y, random_state=7)
    model = LogisticRegression().fit(train_x, train_y)
    return model.score(test_x, test_y)
