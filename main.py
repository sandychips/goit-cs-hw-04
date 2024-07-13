import threading
import multiprocessing
import os
import time
from collections import defaultdict
from multiprocessing import Manager

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Функція для роботи потоку
def worker_thread(files, keywords, results):
    for file_path in files:
        search_keywords_in_file(file_path, keywords, results)

# Основна функція для багатопотокового підходу
def main_threading(file_list, keywords):
    threads = []
    results = defaultdict(list)
    num_threads = min(10, len(file_list))
    chunk_size = len(file_list) // num_threads

    start_time = time.time()

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_threads - 1 else len(file_list)
        thread = threading.Thread(target=worker_thread, args=(file_list[start:end], keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading approach took {end_time - start_time:.2f} seconds")
    return results

# Функція для роботи процесу
def worker_process(files, keywords, results):
    for file_path in files:
        search_keywords_in_file(file_path, keywords, results)

# Основна функція для багатопроцесорного підходу
def main_multiprocessing(file_list, keywords):
    manager = Manager()
    results = manager.dict(defaultdict(list))
    processes = []
    num_processes = min(10, len(file_list))
    chunk_size = len(file_list) // num_processes

    start_time = time.time()

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_processes - 1 else len(file_list)
        process = multiprocessing.Process(target=worker_process, args=(file_list[start:end], keywords, results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Multiprocessing approach took {end_time - start_time:.2f} seconds")
    return dict(results)

# Приклад використання
if __name__ == "__main__":
    file_list = ["file1.txt", "file2.txt", "file3.txt"]  # Вкажіть ваші файли тут
    keywords = ["keyword1", "keyword2"]

    print("Running threading version...")
    results_threading = main_threading(file_list, keywords)
    print(results_threading)

    print("Running multiprocessing version...")
    results_multiprocessing = main_multiprocessing(file_list, keywords)
    print(results_multiprocessing)
