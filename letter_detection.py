import time
import easyocr
import os
"""
Заранее задаем русский алфавит для функции распознавания букв, описанной ниже.
"""
alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р',
            'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'] #список с кириллицей


def letter_writing(image, let_arr):
    """
    Функция для распознания букв на изображении.
    :param image: сделанный дроном снимок.
    :param let_arr: список, в котором хранятся буквы со снимка.
    :return: в случае распознания букв добавляет ее в список и возвращает флаг True, иначе флаг False.
    """
    gpu = False
    reader = easyocr.Reader(['ru'], gpu=gpu) #экземпляр класса easyocr
    result = reader.readtext(image, detail=0) #метод распознавания букв
    if result is None:
        time.sleep(1)
        return None
    else:
        for char in result:
            if any(checking_char.isdigit() for checking_char in char): #проверка на цифры, если они есть, то флаг False
                print('На изображении найдена цифра!')
                time.sleep(1)
                return False
            elif any(checking_letter in alphabet for checking_letter in char):#проверка на буквы, если есть совпадения True
                let_arr.append(char)
                print("К списку присоединена ", char)
                return True
            else: #если ничего нет, то False
                time.sleep(1)
                return False


def decoding(new_word, word):
    """
    Функция для расшифрования полученного слова.
    :param new_word: расшифрованное слово.
    :param word: зашифрованное слово.
    :return: расшифрованное слово.
    """
    for i in range(len(word)):
        for j in range(len(alphabet)):
            if alphabet[j] == word[i]:
                print(alphabet[j])
                if (j + shift) > len(alphabet):
                    new_word += alphabet[j + shift - len(alphabet)]
                elif (j + shift) < 0:
                    new_word += alphabet[len(alphabet) + j + shift]
                else:
                    new_word += alphabet[j + shift]
    return new_word


if __name__ == "__main__":
    try:
        file_shift = open("shift.txt", "r+") #получение ключа
        shift = int(file_shift.read()) #получение ключа
        file_shift.close()
        dirname = 'Photos' #путь к снимкам с предыдущей программы
        word = [] #зашифрованное слово
        new_word = '' #расшифрованное слово
        if os.path.isdir(dirname):
            files = os.listdir(dirname) #чтение файлов с изображениями
            print("Получены файлы: ", files)
            for file in files:
                with open(os.path.join(dirname, file), 'rb+') as f:
                    image = f.read()
                    if letter_writing(image, word): #проверка на буквы
                        print("Сейчас список состоит из: ", word)
                    else:
                        print("На изображении ничего не найдено")
            new_word = decoding(new_word, word)
            print('После расшифровки получилось ', new_word)
        else:
            print('Такой папки не существует')
    except FileNotFoundError: #перехват исключения
        print('Ключа к шифру нет!')
