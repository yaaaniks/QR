import time
import easyocr
import os

alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р',
            'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']


def letter_writing(image, let_arr):
    gpu = False
    reader = easyocr.Reader(['ru'], gpu=gpu)
    result = reader.readtext(image, detail=0)
    if result is None:
        time.sleep(1)
        return None
    else:
        for char in result:
            if any(checking_char.isdigit() for checking_char in char):
                print('На изображении найдена цифра!')
                time.sleep(1)
                return False
            elif any(checking_letter in alphabet for checking_letter in char):
                let_arr.append(char)
                print("К списку присоединена ", char)
                return True
            else:
                time.sleep(1)
                return False


def decoding(new_word, word):
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
        file_shift = open("shift.txt", "r+")
        shift = int(file_shift.read())
        file_shift.close()
        dirname = 'Photos'
        word = []
        new_word = ''
        if os.path.isdir(dirname):
            files = os.listdir(dirname)
            print("Получены файлы: ", files)
            for file in files:
                with open(os.path.join(dirname, file), 'rb+') as f:
                    image = f.read()
                    if letter_writing(image, word):
                        print("Сейчас список состоит из: ", word)
                    else:
                        print("На изображении ничего не найдено")
            new_word = decoding(new_word, word)
            print('После расшифровки получилось ', new_word)
        else:
            print('Такой папки не существует')
    except FileNotFoundError:
        print('Ключа к шифру нет!')
