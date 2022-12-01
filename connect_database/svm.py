from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import numpy as np
from collections import Counter
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
import math


def checkElm(text, keyword):
    array = keyword.split(" ")
    if len(array) == 1:
        for i in text:
            i = i.lower()
            for j in i.split(" "):
                if j == array[0]:
                    return True
        return False

    word = len(array)
    textLength = len(text)
    text.append("asd")
    for i in range(textLength):
        count = 0
        for j in array:
            if text[i].lower().find(j.lower()) != -1 and (
                    text[i].lower().find('không') != -1 or text[i].lower().find('âm tính') != -1 or text[
                i + 1].lower().find('(-)') != -1):
                return False

            if text[i].lower().find(j.lower()) != -1:
                count += 1
                if count == word:
                    return True

    return False


def finding(text, keywords):
    keywords = keywords.split('|')
    for key in keywords:
        key = key.strip()
        if checkElm(text, key):
            return True
    return False


def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1


def getField(keyword, sign, to, para, text_keyword, array):
    para = para.lower()
    par = para
    check = False
    # Kiểm tra từ keyword và sau nó 6 kí tự xem có sign hay không
    id1 = 0
    if para.find(keyword) == -1:
        array.append(0)
        return

    while check == False and para != "":
        if para.find(keyword) != -1:
            id1 = para.find(keyword)  # Tìm vị trí của keyword

        para = para[(id1 + 3):]  # Giảm độ dài đoạn text nếu không có keyword và sign
        if para != "":
            par = para

    if to != "":
        new_para = par[:par.find(to)]
    else:
        new_para = par

    if new_para[:20].find(sign) != -1:
        new_array = splitText(new_para)
        hasSignal(new_array, text_keyword, array)
    else:
        array.append(0)
        return


# Phân tích đoạn text thành từng đoạn (cách nhau bởi các chữ viết hoa và dấu phẩy)
# VD: Text: "Lúc vào : Bệnh nhân tỉnh, thể trạng trung bình Da"
# --->   ['', ' Lúc  vào ', ' : ', ' Bệnh  nhân  tỉnh, ', ' thể  trạng  trung  bình ', ' Da ']
def splitText(text):
    text = text + " H"
    word = text.replace("\n", " ")
    word1 = word.split(" ")
    word2 = []

    for i in word1:
        if (i.isupper()):
            word2.append(i)
        else:
            word2.append(i.capitalize())
    result = []  # Lưu từng câu
    text = ""

    for i in range(len(word1)):
        if word1[i] == word2[i] or word1[i - 1].find(",") != -1:
            result.append(text)
            text = ""
        text = text + " " + word1[i] + " "
    return result


def hasSignal(paragraph, keyword, signal):
    if finding(paragraph, keyword):
        signal.append(1)
    else:
        signal.append(0)


def getArray(arr1, arr2):
    arr = []
    for i in range(len(arr1)):
        if arr1[i] == 1 or arr2[i] == 1:
            arr.append(1)
        else:
            arr.append(0)
    return arr


def getExpression(array):
    check = 0
    express = ["đau bụng", "nôn", "chán ăn", "táo bón", "tiêu chảy", "phân nhỏ",
               "phân có máu", "sút cân", "da niêm mạc bình thường", "da niêm mạc vàng",
               "da sạm", "hoạch ngoại biên", "hạch thường đòn", "tiền sử ung thư",
               "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc", "dấu hiện rắn bò",
               "quai ruột nổi", "sờ thấy khối u", "thăm trực tràng có khối u", "chụp CT ổ bụng có khối u",
               "nội soi đại tràng có khối u"]

    commit = ""
    for i in range(len(array)):
        if array[i] == 1:
            check += 1
            commit = commit + express[i] + ", "

    if check == 0:
        return ""

    chain = commit[0].upper() + commit[1:len(commit) - 2] + "."
    return chain


def call_mining(data_frame):
    data_list = data_frame["dienbiengaydautien"]
    d_list = []
    for i in data_list:
        nul = False
        try:
            nul = math.isnan(float(i))
        except:
            d_list.append(str(i))
            continue
        if nul == True:
            continue
        else:
            d_list.append(str(i))
    return mining(d_list)


def mining(data):
    # Tạo các mảng lưu thông tin cho các trường tương ứng
    dau_bung = []
    non = []
    chan_an = []
    tao_bon = []
    tieu_chay = []
    phan_nho = []
    phan_co_mau = []
    giam_can = []
    da_niem_mac_bt = []
    da_sam = []
    da_niem_mac_vang = []
    hoach_ngoai_bien = []
    hach_thuong_don = []
    tien_su_ung_thu = []
    bung_chuong = []
    pu_thanh_bung = []
    cu_phuc_mac = []
    dh_ran_bo = []
    quai_ruot_noi = []
    so_thay_khoi_u = []
    tham_tt_co_u = []

    noi_soi_dai_tran_cou = []
    sa = []
    ns = []

    chup_ct_o_bung_cou = []
    ct1 = []
    ct2 = []

    chan_doan = []
    cd1 = []
    cd2 = []

    # Lưu giá trị vào các mảng tư sau mỗi lần chạy qua dữ liệu
    for i in data:
        getField("nội soi", ":", "chẩn đoán", i, "u | k ", ns)
        getField("siêu âm", ":", "chẩn đoán", i, "u | k ", sa)
        noi_soi_dai_tran_cou = getArray(ns, sa)

        getField("thăm trực tràng", ":", "chẩn đoán", i, "u | k ", tham_tt_co_u)

        getField("ct scanner", ":", "chẩn đoán", i, "u | k ", ct1)
        getField("ctscanner", ":", "chẩn đoán", i, "u | k ", ct2)
        chup_ct_o_bung_cou = getArray(ct1, ct2)

        getField("đoán", ":", "", i, "u|k|ung thư", cd1)
        getField("đoán", ";", "", i, "u|k|ung thư", cd2)
        chan_doan = getArray(cd1, cd2)

        p = splitText(i)
        hasSignal(p, "chẩn đoán", chan_doan)
        hasSignal(p, "đau bụng", dau_bung)
        hasSignal(p, "nôn", non)
        hasSignal(p, "ăn kém", chan_an)
        hasSignal(p, "táo bón | đại táo | phân táo ", tao_bon)
        hasSignal(p, "tiêu chảy | phân lỏng", tieu_chay)
        hasSignal(p, "phân nhỏ", phan_nho)
        hasSignal(p, "phân máu", phan_co_mau)
        hasSignal(p, "sút cân | giảm cân", giam_can)
        hasSignal(p, "niêm mạc hồng | niêm mạc nhẹ | niêm mạc nhợt", da_niem_mac_bt)
        hasSignal(p, "niêm mạc vàng", da_niem_mac_vang)
        hasSignal(p, "da sạm | da xạm | da xanh", da_sam)
        hasSignal(p, "ngoại biên", hoach_ngoai_bien)
        hasSignal(p, "thượng đòn", hach_thuong_don)
        hasSignal(p, "đã ung thư", tien_su_ung_thu)
        hasSignal(p, "bụng chướng", bung_chuong)
        hasSignal(p, "thành bụng", pu_thanh_bung)
        hasSignal(p, "phúc mạc", cu_phuc_mac)
        hasSignal(p, "rắn bò", dh_ran_bo)
        hasSignal(p, "quai ruột nổi", quai_ruot_noi)
        hasSignal(p, "sờ thấy u", so_thay_khoi_u)

        if len(i) < 30:
            chan_doan.pop()
            chan_doan.append(0)


    # Lưu các feature
    feature = [dau_bung, non, chan_an, tao_bon, tieu_chay, phan_nho, phan_co_mau, giam_can, da_niem_mac_bt, da_sam,
               da_niem_mac_vang, hoach_ngoai_bien, hach_thuong_don, tien_su_ung_thu, bung_chuong, pu_thanh_bung,
               cu_phuc_mac, dh_ran_bo, quai_ruot_noi, so_thay_khoi_u, tham_tt_co_u, chup_ct_o_bung_cou,
               noi_soi_dai_tran_cou]

    return [feature, chan_doan]


def train(feature, chan_doan):
    for i in range(17):
        chan_doan.append(0)

    for k in range(17):
        for i in feature:
            if i == feature[k]:
                i.append(1)
            else:
                i.append(0)

    for i in feature:
        i.append(0)

    for n in range(800):
        for i in range(len(feature)):
            feature[i].append(0)
        chan_doan.append(0)

    feature_col = np.array(feature).T
    # ---------------------------------

    # Sử dụng smote để tái cân bằng dữ liệu
    counter = Counter(chan_doan)
    print(counter)

    if counter.get(0)/counter.get(1) < 0.4 or counter.get(1)/counter.get(0) < 0.4:
        over = SMOTE(sampling_strategy=0.8)  #lấy 80% lớp đa số
        under = RandomUnderSampler(sampling_strategy=0.8) #lấy lớp thiếu số có số lượng = 80% lớp đa số
        steps = [('o', over), ('u', under)]
        pipeline = Pipeline(steps=steps)

        # transform the dataset
        feature_col, chan_doan = pipeline.fit_resample(feature_col, chan_doan)

    counter = Counter(chan_doan)
    print(counter)
    print("-" * 50)

    # Phân chia dữ liệu và chạy chẩn đoán
    x_train, x_test, y_train, y_test = train_test_split(feature_col, chan_doan
                                                        , test_size=0.2, random_state=100)
    classifier = svm.SVC(kernel='rbf')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    print("Độ chính xác: ", metrics.accuracy_score(y_pred, y_test))
    metrx = confusion_matrix(y_pred, y_test)

    # Dự đoán -> Thực tế
    # [1, 1]:   Dương tính - thật
    # [1, 2]:   Âm tính - giả
    # [2, 1]:   Dương tính - giả
    # [2, 2]:   Âm tính - thật
    print(metrx)
    print("Độ nhạy: " + str(metrx[1][1] / (metrx[1][1] + metrx[1][0])))
    print("Độ đặc hiệu: " + str(metrx[0][0] / (metrx[0][0] + metrx[0][1])))
    print("-" * 50)
    print("Dự đoán thử nghiệm: ")
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(arr)
    y_pred = classifier.predict([arr])
    print("Kết quả: ", y_pred)
    print("Triệu chứng: " + getExpression(arr))
    return classifier