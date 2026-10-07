class Seq:
    """
    Создаем класс для представления биологических последовательностей.  
    Хранит информацию о заголовке записи и саму биологическую последовательность
    """
    def __init__(self, fasta_str, sequence):
        """Инициализирует объект последовательность.
        fasta - строка заголовка FASTA (без знака ">")
        sequence - строка последовательности"""
        self.fasta = fasta_str.strip()
        self.sequence = sequence.strip()
    
    @property
    def fasta_length(self):
        """Возвращает точную длину биологической последовательности"""
        return len(str(self.sequence))

    @property
    def final_sequence(self):
        """
        Форматирует последовательность для вывода.
                Если длина превышает 60 символов, разбивает её 
                на строки по 60 символов с переносом строки.
                Возвращает:
                    str: Отформатированная биологическая последовательность.
        """
        subseq = str(self.sequence)
        final_subseq = []
        if len(subseq) > 60:
            for i in range(0, len(subseq), 60):
                chunk = subseq[i: i+60]
                final_subseq.append(chunk)
            return "\n".join(final_subseq)
        return subseq

    @property
    def alphabet(self):
        """
        Определяет тип алфавита последовательности.
        Возвращает:
            Нуклеотид - если в строке только буквы ДНК/РНК (A, C, G, T, U, N).
            Белок - если найдены любые другие аминокислотные буквы.
        """
        nucleotides = "ACGTUN"
        subsequence = self.sequence
        for symbol in subsequence:
            if symbol not in nucleotides:
                return("Белок")
        return("Нуклетотидная последовательность")

class Fasta_Reader:
    """Класс для потокового чтения файлов формата FASTA."""
    def __init__(self, file_path):
        """
        Инициализируем функцию для чтения конкретного файла.
        file_path - путь к файлу
        """
        self.file_path = file_path
    def check_seq(self):
        """
        Проверяет, соответствует ли файл базовому формату FASTA.
        Возвращает True, если файл успешно открылся и его первая непустая строка начинается с символа '>', 
        иначе False.
        """
        try:
            with open(self.file_path) as file:
                for line in file:
                    line = line.strip()
                    if line != "":
                        return line.startswith(">")
            return False
        except (FileNotFoundError, IOError):
            return False

    def read_seq(self):
        """
        Считывает биологические последовательности из файла (формат FASTA) и возвращает объекты Seq.
        Построчно обрабатывает файл, группируя строки последовательности 
        под соответствующими заголовками (идентификаторами), начинающимися с '>'.
        Yields:
            Seq: Объект последовательности, содержащий имя (заголовок) и саму последовательность.
        """
        current_name = ""
        current_seq_lines = ""
        with open(self.file_path) as file:
            for line in file:
                if line == "":
                    continue 
                if line.startswith(">"):
                    if current_name != "":
                        yield Seq(current_name, current_seq_lines)
                        current_seq_lines += ""
                    current_name = line[1:]
                else:
                    current_seq_lines += line.strip()
            if current_seq_lines:
                yield Seq(current_name, current_seq_lines)

"ДЕМОНСТРАЦИЯ РАБОТЫ ПРОГРАММЫ"
file_name = "/home/vboxuser/Downloads/NM_000558.5.fna"
reader = Fasta_Reader(file_name)
if reader.check_seq() == True:
    print("Файл успешно прошел проверку! Данный файл - FASTA формата.")

    for j in reader.read_seq():
        print("Имя FASTA-файла:")
        print(j.fasta)

        print("Длина последовательности:")
        print(j.fasta_length)

        print("Тип последовательности:")
        print(j.alphabet)

        print("Биологическая последовательность:")
        print(j.final_sequence)
else:
    print("Ошибка! Файл не найден или не в fasta формате")

    

    

    


