from pioneer_sdk import Pioneer, Camera
import cv2
import time
import os


def read_qr(buffer_coordinates, camera_frame): #функция для чтения qr-кодов
    detector = cv2.QRCodeDetector() #задаем класс cv для чтения qr-кодов
    string, _, _ = detector.detectAndDecode(camera_frame)
    if string: #если есть точка, значит получаем координаты в виде строки
        if len(string) == 1 or len(string) == 2:  # если полученная длина равна 1 или 2,
            return 0, int(string), True  # значит возвращаем ключ от шифра, обнуляем буфер и флаг на окончание полета
        text = string.split() #получаем список с коордианатами, разделяя строку пробелом
        for i in range(len(text)): #перезаписываем список строчного типа в список типа float
            text[i] = float(text[i])/1.5
        if text != buffer_coordinates: #если координаты еще не были получены, значит возваращаем их, новый буфер и флаг на окончание полета
            return text, text, False
        else: #если координаты были, значит отправляем дрону команду на окончание полета
            print("[INFO] Такие координаты уже были получены!")
            return 0, 0, True
    else: #если ничего нет
        return None


def drone_flight(drone, camera_ip): #основная функция скрипта
    global list_of_cor, finish, buff  #задаем начальные данные
    buff = 0 #буфер для хранения координат
    list_of_cor = [] #список получаемых координат
    counter = 1 #счетчик для корректного сохранения фотографий
    finish = False #флаг на завершение полета
    command_x = 0
    command_y = 0
    time_counter = 0 #счетчик времени
    flight_height = float(1)
    new_point = True
    while True: #бесконечный цикл
        camera_frame = camera_ip.get_cv_frame() #получаем снимок с камеры дрона
        # cv2.imshow('flight', camera_frame) #выводим в отдельное окно
        if new_point: #если флаг на новую точку с qr-кодом, то отправляем команду дрону лететь на эту метку
            drone.go_to_local_point(x=command_x, y=command_y, z=flight_height, yaw=0)
            new_point = False
        if drone.point_reached(): #если заданная точка достигнута
            time.sleep(1)
            while time_counter<3:
                camera_frame = camera_ip.get_cv_frame()
                if read_qr(buff, camera_frame) is not None: #если qr-код обнаружен
                    buff, list_of_cor, finish = read_qr(buff, camera_frame) #получаем новый буффер с координатами последней
                    print("[INFO] Получен набор координат: ", list_of_cor)  #точки, новые координаты и флаг на окончание
                    break
                time_counter+=1
                time.sleep(1)
            time_counter = 0 #обнуляем счетчик времени
            if finish: #если в qr-коде ключ от шифра
                file_shift = open("shift.txt", "w+") #создание текстового файла
                file_shift.write(str(list_of_cor)) #запись в него ключа
                file_shift.close()
                break
            elif list_of_cor: #если в qr-коде координаты точек
                if list_of_cor[2] != 0 or list_of_cor[3] != 0:
                    print("[INFO] Дрон направляется к " + str(counter) + " точке")
                    drone.go_to_local_point(x=list_of_cor[2], y=list_of_cor[3], z=flight_height, yaw=0)
                    while True:
                        image = camera_ip.get_cv_frame() #получаем снимок с точки, где расположена буква
                        if drone.point_reached(): #если заданная точка достигнута
                            time.sleep(1)
                            cv2.imwrite('Photos/point' + str(counter) + '.jpg', image) #сохраняем снимок буквы с названием точки
                            print('success ', counter)
                            counter += 1
                            break
                    if list_of_cor[4] != 0 or list_of_cor[5] != 0:
                        print("[INFO] Дрон направляется к " + str(counter) + " точке")
                        drone.go_to_local_point(x=list_of_cor[4], y=list_of_cor[5], z=flight_height, yaw=0)
                        while True:
                            image = camera_ip.get_cv_frame() #получаем снимок с точки, где расположена буква
                            if drone.point_reached(): #если заданная точка достигнута
                                time.sleep(1)
                                cv2.imwrite('Photos/point' + str(counter) + '.jpg', image) #сохраняем снимок буквы с названием точки
                                print('success ', counter)
                                counter += 1
                                command_x = list_of_cor[0]  # задаем координату x новой точки с qr-кодом
                                command_y = list_of_cor[1]  # задаем координату y новой точки с qr-кодом
                                list_of_cor.clear()  # обуляем список координат
                                new_point = True  # обновляем флаг на новую точку
                                break
            else:
                print("[INFO] Координаты не заложены в набор команд")
                break


if __name__ == '__main__':
    Photos = os.path.join(os.getcwd(), "Photos")  # создаёт папку Photos для сохранения фотографий
    if not os.path.isdir(Photos):
        os.mkdir(Photos)

    pioneer_mini = Pioneer()  # pioneer_mini как экземпляр класса Pioneer
    camera = Camera() #camera как экземпляр класса Camera
    pioneer_mini.arm()
    pioneer_mini.takeoff()

    drone_flight(pioneer_mini, camera)

    pioneer_mini.land() #сажаем дрон
    time.sleep(2)
    cv2.destroyAllWindows()  # закрывает окно с выводом изображения
    exit(0)