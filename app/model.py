import pandas as pd
pd.options.display.max_columns = 100
pd.options.display.max_rows = 1000
from sklearn import preprocessing
from sklearn.externals import joblib
import os
from datetime import datetime
# для сохранения и загрузки сложных объектов

column_X = ['m', 'TEMP', 'time', 'VALC', 'VALSI', 'VALMN',
       'VALP', 'VALS', 'VALAL', 'VALALS', 'VALCU', 'VALCR', 'VALMO',
       'VALNI', 'VALV', 'VALTI', 'VALNB', 'VALCA', 'VALCO', 'VALPB',
       'VALW', 'VALCE', 'VALB', 'VALAS', 'VALSN', 'VALBI', 'VALZR',
       'VALO', 'VALN', 'W', 'Известь собственного производства2',
       'Шрам 752', 'MnSi17А2', 'ФХ0252',
       'Графит искусственный 0,1-2,5 мм2', 'Al проволока (АПВ)2',
       'FeV-502', 'ПП-СК30 проволока2', 'алюминий вторичный АВ 872',
       'ФМН 78 ГОСТ4755-91 класс 42', 'FeSi65-42', 'BIOTEX2', 'АТФ-752',
       'Кокс 10-30 мм2', 'Ферротитан ФТ702', 'Izomix2',
       'Ферротитан ФТ352', 'АВ-87 брикеты2', 'Гранулы АВ-872',
       'Ферромолбден ФМо 602', 'Феррониобий ФНб 602', 'СИМП-РМ2',
       'ФВд802', 'известь 2 сорт2', 'Лигатура ванадиевая2',
       'FeCa 70 проволока2', 'ферроцерий2', 'Мн 952',
       'Лигатура ниобиевая ФНСБ2', 'ФОМИ Б22', 'Магма2', 'АШМ 752',
       'серная проволока2', 'glutin sp/m-10b2', 'АКСФ2',
       'КРС-65 брикеты2', 'CaF2-922', 'СК402', 'Стружка сплава титана2',
       'Брикет Алюминиевый2', 'Проволока ПП-Т-14, 15 Графит ТУ 1479-0122',
       'Никель гранулир.2', 'Проволока ферротитановая2',
       'Лом сплава титана2', 'Гранулят Мо2', 'Ферромолбден ФМо 502',
       'Проволока порошковая ФВд502', 'КШУ 752', 'ФСВд 252', 'FeCr 850А2',
       '25A2', 'Б-675 титан2', 'Флюс глиноземистый2', 'C 0,5-2,5 mm2',
       'Катализатор КВ-1, 10-20%2', 'Проволока ферромолибденовая2',
       'брикет БМК-602', 'Феррохром высокоуглеродистый2', 'АТФ-75Б2',
       'Проволока Fe-B2', 'Марш-752', 'Сплав ванадия с железом2',
       'Известь2', 'ФС 452', 'ФСХ 402', 'Алюминий АВ-87 пирамидки2',
       'АТФ-A2', 'Гранулы АГВ2', 'УСМ 03-10мм2',
       'Проволока феррониобиевая2', 'СШУ-1Г2', 'Алюминий втор АВК-65Ф2',
       'Материал теплоизолирующий ТПК-ПК2', 'катанка алюмин АКЛП2',
       'Концентрат ванадиевый ВКПЛ-102', 'Флюс ФМ-2-12', 'Материал ФГМ2',
       'флюс МВП2']

column_y = ['TEMP2','VALC2', 'VALSI2', 'VALMN2', 'VALP2', 'VALS2',
       'VALAL2', 'VALALS2', 'VALCU2', 'VALCR2', 'VALMO2', 'VALNI2',
       'VALV2', 'VALTI2', 'VALNB2', 'VALCA2', 'VALCO2', 'VALPB2', 'VALW2',
       'VALCE2', 'VALB2', 'VALAS2', 'VALSN2', 'VALBI2', 'VALZR2', 'VALO2',
       'VALN2']

def main(file, username):
    predict = pd.DataFrame(columns=column_y)
    path = os.getcwd()
    for i in column_y:
        GB = joblib.load(path +'/app/model_GB/GB_'+i+'.pkl')
        tit = joblib.load(path +'/app/model_GB/titles_'+i+'.json')
        sc = preprocessing.StandardScaler()
        sc = joblib.load(path+'/app/model_GB/scaler_'+i)
        table = pd.read_excel(file)
        now = datetime.now()
        time = "%d_%ddate %d_%d_%dtime" % (now.day, now.month, now.hour, now.minute, now.second)
        input_filename = os.getcwd() + '/app/input/' + "input_" + time + "_" + username + ".xlsx"
        table.to_excel(input_filename)

        table = table.fillna(0)
        X = table[column_X]
        X_transform = sc.transform(X)
        y_predict = GB.predict(X_transform)
        predict[i] = y_predict
    output_filename = os.getcwd() + "/app/output/output" + time + "_" + username + '.xlsx'
    predict.to_excel(output_filename)