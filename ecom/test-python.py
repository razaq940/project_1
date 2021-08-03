from datetime import datetime
import json

def main():
    waktu_sekarang = datetime.now()
    print(waktu_sekarang)

main()


# no 2
def main2():
    data = input("Maukan angka dengan koma: ")
    data_tuple = tuple(int(x) for x in data.split(","))
    data_list = list(int(x) for x in data.split(","))
    print(data_list)
    print(data_tuple)

main2()

#no 3

json_obj =  '{ "Nama":"Abdul", "Kelas":"I", "Usia":26 }'
python_obj = json.loads(json_obj)
print("\nJSON data:")
print(python_obj)
print("\nNama: ",python_obj["Nama"])
print("Kelas: ",python_obj["Kelas"])
print("Usia: ",python_obj["Usia"]) 


#no 4
nama1 = "abdul"
kelas1 = "I"
usia1 = 26
list1 = [nama1,kelas1,usia1]
print(json.dumps(list1))

#no 5
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

even = 0
odd = 0
for i in numbers:
    if(i % 2 == 0):
        even += 1
    else:
        odd += 1
print("{0} even numbes and {1} odds.".format(even, odd))