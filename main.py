#!/usr/bin/env python
# -*- coding: utf-8 -*-


def convert_data_to_list_of_int(data):
    return [int(d) for d in data.split()]


def pack_libraries_with_boks(libraries_and_books):
    libs_packed = []

    for i in range(0, len(libraries_and_books), 2):
        current_lib = libraries_and_books[i:i+2]
        libs_packed.append(current_lib)
    
    for i, lib in enumerate(libs_packed):
        lib.append(i)

    return libs_packed


INPUT_FILES_NAMES = ["a_example.txt", "b_read_on.txt", "c_incunabula.txt",
                     "d_tough_choices.txt", "e_so_many_books.txt", "f_libraries_of_the_world.txt"]
OUTPUT_FILE_NAMES = ["a_example_out.txt", "b_read_on_out.txt", "c_incunabula_out.txt",
                     "d_tough_choices_out.txt", "e_so_many_books_out.txt", "f_libraries_of_the_world_out.txt"]
FILE_NAME_INDEX = 4


def main():
    raw_data = []
    with open("input/" + INPUT_FILES_NAMES[FILE_NAME_INDEX]) as f:
        raw_data = f.read().strip().split("\n")

    book_num_libraries_days = convert_data_to_list_of_int(raw_data.pop(0))
    book_scores = convert_data_to_list_of_int(raw_data.pop(0))

    libraries_and_books = [convert_data_to_list_of_int(data) for data in raw_data]

    libs_packed_unsorted = pack_libraries_with_boks(libraries_and_books)

    libs_packed =  sorted(libs_packed_unsorted, key=lambda x: x[0][1])

    # print([print("index: " + str(i) + " " + str(libs[0])) for i, libs in enumerate(libs_packed)])

    # print(libs_packed)

    days = book_num_libraries_days[2]

    current_lib_under_signup = None
    scanned_books = []
    signup_is_going = False
    scannable_libs = []
    current_signup_count = None
    packed_scanned_books = []
    lib_order = []

    for day in range(days):
        # print("Day {}".format(i))
        if not signup_is_going:
            current_lib_under_signup = libs_packed.pop(0)
            signup_is_going = True
            current_signup_count = current_lib_under_signup[0][1]

        if(current_signup_count > 0):
            current_signup_count -= 1
        else:
            signup_is_going = False
            scannable_libs.append(current_lib_under_signup)
            current_lib_under_signup = None

        for lib_id, lib in enumerate(scannable_libs):
            scan_count = lib[0][2]
            books = lib[1]
            id_of_the_lib = lib[2]
            if id_of_the_lib not in lib_order:
                lib_order.append(id_of_the_lib)

           
            for scanned in scanned_books:
                if scanned in books:
                    books.remove(scanned)

            for i in range(scan_count):
                if books:
                    book = books.pop(0)
                    scanned_books.append(book)
                    try:
                        packed_scanned_books[lib_id].append(book)
                    except IndexError:
                        packed_scanned_books.append([])
                        packed_scanned_books[lib_id].append(book)
                else:
                    break


    with open('output/' + OUTPUT_FILE_NAMES[FILE_NAME_INDEX], 'w+') as f:
        f.write(str(len(packed_scanned_books)) + "\n")
        for i, pack in enumerate(packed_scanned_books):
            f.writelines("{} {}\n".format(lib_order[i], len(pack)))
            for book in pack:
                f.write(str(book) + " ")
            f.write("\n")


if __name__ == "__main__":
    main()
