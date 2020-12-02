from collections import defaultdict
from typing import Dict, List, Union, Tuple, Set
import math
import traceback
import random


class Word:
    def __init__(self, syllables: int, value: str):
        self.syllables = syllables
        self.value = value

    def __repr__(self):
        return f'<Word value={self.value}, syllables={self.syllables}>'

    def __len__(self):
        return len(self.value)


class Words(list):
    def __init__(self, *words: Word):
        super().__init__(words)
        self._words_counter = 0
        self.words_with_types: defaultdict[int, List[Dict[int, Word]]] = \
            defaultdict(list)
        for i in range(len(words)):
            self.words_with_types[words[i].syllables].append({
                i + self._words_counter: words[i]
            })
        self._words_counter += len(words)

    def extend(self, words: Union[List[Word], Tuple[Word], Set[Word]]):
        super().extend(words)
        for i in range(len(words)):
            self.words_with_types[words[i].syllables].append({
                i + self._words_counter: words[i]
            })
        self._words_counter += len(words)

    def append(self, word: Word):
        super().append(word)
        self.words_with_types[word.syllables].append({
            self._words_counter: word
        })
        self._words_counter += 1


class Task:
    @classmethod
    def run(cls, mode: int, total_words_count: int = 16):
        words = Words()

        max_word_len = 0

        if mode == 2:
            words_types = (1, 2)
        elif mode == 3:
            words_types = (1, 3)
        elif mode == 4:
            words_types = (3, 4)
        else:
            raise ValueError(f'Режима {mode} не существует')

        for words_type in words_types:
            words_in_file = []
            with open(f'words{words_type}.txt', encoding='utf8') as f:
                file_str = f.read()

            for word_value in file_str.split('\n'):
                words_in_file.append(Word(words_type, word_value))

                if len(word_value) > max_word_len:
                    max_word_len = len(word_value) + 10

            words.extend(random.sample(
                words_in_file,
                total_words_count // 2
                if len(words) == 0
                else total_words_count - len(words),
            ))

        random.shuffle(words)
        words = Words(*words)

        print(
            '\n\n'
            'Слушателю надо продиктовать слова по одному, '
            'а он должен записывать на листочек номера слов:'
        )
        for i in range(total_words_count):
            print(f'#{i + 1} {words[i].value}')
        print('\n')

        print('Что в итоге должно получиться (правильные ответы):\n')

        first_type_header = cls.get_syllables_with_ending(words_types[0])
        second_type_header = cls.get_syllables_with_ending(words_types[1])
        header = (
            f' {first_type_header}'
            + ' ' * (max_word_len - len(first_type_header)) + ' | '
            + second_type_header
            + ' ' * (max_word_len - len(second_type_header) + 1)
        )
        print(header)
        print('-' * len(header))

        rows_count = math.ceil(total_words_count / 2)
        for i in range(rows_count):
            if len(words.words_with_types[words_types[0]]) <= i:
                first_type_word = ''
            else:
                record = words.words_with_types[words_types[0]][i].items()
                first_type_number, first_type_word = next(iter(record))
                first_type_word = first_type_word.value
                first_type_number = str(first_type_number + 1)
                first_type_number += (
                    '  ' if len(first_type_number) == 1 else ' '
                )

            left_col = f'{first_type_number} {first_type_word}'
            left_col += ' ' * (max_word_len - len(left_col))

            if len(words.words_with_types[words_types[1]]) <= i:
                second_type_word = ' ' * max_word_len
            else:
                record = words.words_with_types[words_types[1]][i].items()
                second_type_number, second_type_word = next(iter(record))
                second_type_word = second_type_word.value
                second_type_number = str(second_type_number + 1)
                second_type_number += (
                    '  ' if len(second_type_number) == 1 else ' '
                )

            right_col = f'{second_type_number} {second_type_word}'
            right_col += ' ' * (max_word_len - len(right_col))

            print(f' {left_col} | {right_col}')

    @staticmethod
    def get_syllables_with_ending(syllables: int) -> str:
        if syllables == 1:
            return f'{syllables} слог'
        return f'{syllables} слога'


def setup():
    for i in range(1, 4):
        try:
            open(f'words{i}.txt').close()
        except Exception as e:
            print(f'Не найден файл words{i}.txt в директории с текущим файлом')
            raise

    mode = None
    while mode not in (2, 3, 4):
        if mode is not None:
            print('\nВы должны ввести один из перечисленных вариантов!\n')

        print(
            'Добро пожаловать! \n'
            'Выберите режим использования:\n'
            '  2 - слова с одним и двумя слогами\n'
            '  3 - слова с одним и тремя слогами\n'
            '  4 - слова с тремя и четыремя слогами\n'
        )
        input_text = (
            'Ваш выбор (введите цифру): '
            if selected_mode is None
            else f'Ваш выбор (по умолчанию {selected_mode}): '
        )
        mode = input(input_text)
        if mode.isdigit():
            mode = int(mode)
        elif mode == '' and selected_mode is not None:
            mode = selected_mode

    print('')

    total_words_count = None
    while type(total_words_count) != int:
        total_words_count = input(
            'Теперь выберите сколько хотите слов '
            f'(по умолчанию - {selected_total_words_count or 16}): '
        )
        if total_words_count == '':
            total_words_count = (
                16
                if selected_total_words_count is None
                else selected_total_words_count
            )
        elif total_words_count.isdigit():
            total_words_count = int(total_words_count)
            if total_words_count <= 1:
                print('\nНеобходимо ввести число от 2 и больше!')
                total_words_count = None
        else:
            print(
                '\nВы должны ввести число или '
                'нажимите Enter для значения по умолчанию!\n'
            )

    return mode, total_words_count


if __name__ == '__main__':
    selected_mode = selected_total_words_count = None
    try:
        while True:
            selected_mode, selected_total_words_count = setup()
            Task.run(selected_mode, selected_total_words_count)
            print('')
            restart_input = input(
                'Для нового запуска нажимите Enter или введите любой текст, '
                'чтобы закрыть программу: '
            )
            if restart_input != '':
                exit(0)
    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        traceback.print_exc()
        print('Произошла ошибка')
        input('Нажмите Enter для выхода...')
        exit(1)
