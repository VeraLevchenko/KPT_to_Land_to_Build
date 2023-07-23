import xml.etree.ElementTree as ET
import os

# функция возвращает список .xml файлов из папки, включая подпапки, кроме proto_.xml
def get_file_list(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xml") and file != "proto_.xml":
                filelist.append(os.path.join(root, file))
    return filelist


#  MIF Функция парсит кпт и вытаскивает количество контуров, количество точек и их координаты
def make_list_for_mif_actual_build(file_name):
    list_build = []
    tree = ET.parse(file_name)
    # ------------------------------возвращает список участков----------------------------------------------
    build_records = tree.findall('cadastral_blocks/cadastral_block/record_data/base_data/build_records/build_record')
    for build_record in build_records:
        #  ---------------------------возвращает список контуров в каждом участке----------------------------
        contours = build_record.findall("./contours/contour")
        if len(contours) > 0:
            list_build.append("Region ")
            list_build.append(len(contours))
            for contour in contours:
                # ---------------возвращает список координат точек в каждом контуре в каждом участке---------
                ordinates = contour.findall("./entity_spatial/spatials_elements/spatial_element/ordinates/ordinate")
                list_build.append(len(ordinates))
                # возращаем значение координат из списка
                for ordinate in ordinates:
                    y = ordinate.find('y').text
                    x = ordinate.find('x').text
                    list_build.append(y)
                    list_build.append(x)
    return list_build


#  MIF Функция печатает в файл mif заголовочные данные
def print_head_mif():
    file_mif_head = open('D:/KPT/_Example/actual_build.mif', 'a')
    head_data = [
        'Version   450',
        'Charset "WindowsCyrillic"',
        'Delimiter ","',
        'CoordSys Earth Projection 8, 1001, "m", 88.466666, 0, 1, 2300000, -5512900.5630000001 '
        'Bounds (-5949281.53901, -15515038.0608) (10549281.539, 4489236.93476)',
        'Columns 7',
        'type Char(30)',
        'purpose Char(100)',
        'cad_number Char(30)',
        'readable_address Char(254)',
        'area Char(50)',
        'cost Char(50)',
        'date_download Char(10)',
        'Data'
        ]
    for index in head_data:
        file_mif_head.write(index + '\n')
    file_mif_head.close()


def make_list_for_mid_actual_build(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    request = root[1][0].text
    list_semantic_build = ''
    data = tree.findall('cadastral_blocks/cadastral_block/record_data/base_data/build_records/build_record')
    for data1 in data:
        #  ------------------- проверка на наличие координат границ------------------------------------------
        coordinates = data1.findall("./contours/contour")
        if len(coordinates) > 0:
            #  -------------------Тип объекта------------------------------------------
            data2 = data1.findall('./object/common_data/type/value')
            if len(data2) >= 1:
                for tipe in data2:
                    _type = tipe.text
            else:
                _type = "None"
            #  -------------------Кадастровый номер------------------------------------------
            if len(data3) >= 1:
                for cad_number in data3:
                    _cad_number = ca_d_number.text
            else:
                _cad_number = "None"
            #  -------------------Адрес-------------------------------------------
            if len(data4) >= 1:
                for adress in data4:
                    _adress = adress.text
                    rez_adress = _adress.replace('"', '\'')
            else:
                _adress = "None"
            data5 = data1.findall('params/purpose/value')
            if len(data5) >= 1:
                for purpose in data5:
                    _purpose = purpose.text
                _purpose = "None"
            #  --------------------Площадь------------------------------------------
            data6 = data1.findall('params/area')
            if len(data6) >= 1:
                for area in data6:
                    _area = area.text
            else:            #  --------------------Цена------------------------------------------
            date7 = data1.findall('./cost/value')

                    _area = "None"
            if len(date7) >= 1:
                for cost in date7:
                    _cost = cost.text
            else:
                _cost = "None"
            # Формирует строку mid файла
            a = ("\"" + _type[:30] +
                 "\"," + "\"" + _purpose[:100] +
                 "\"," + "\"" + _cad_number[:30] +
                 "\"," + "\"" + rez_adress[:250] +
                 "\"," + "\"" + _area[:50] +
                 "\"," + "\"" + _cost[:50] +
                 "\"," + "\"" + request +
                 "\"," + "\n")
cc            list_semantic_build = (list_semantic_build + a)
    return list_semantic_build
if __name__ == '__main__':
    print_head_mif()
# -------------------------Открываем поочередно кпт.xml файлы----------------------------------
    filelist = get_file_list("D:/KPT")
    i = 1
    for file_name in filelist:
        print("Идет выгрузка, подождите ", (i * 100) / len(filelist), "% ... ")  # Проверка пути!!!!!!!!!!!!!!!!
        i += 1
        file_mif = open('D:/KPT/_Example/actual_build.mif', 'a')
# ------------------------записываем полученный список в mif файл-------------------------------
        list_coordinate_build_record = make_list_for_mif_actual_build(file_name)
        for data8 in list_coordinate_build_record:
           file_mif.write(str(data8) + '\n')
        file_mif.close()
# ---------------------------записываем данные mid в файл---------------------------------------
        build = make_list_for_mid_actual_build(file_name)
        file_mid = open('D:/KPT/_Example/actual_build.mid', 'a')
        file_mid.write(build)
        file_mid.close()
