
import matplotlib.pyplot as plt
import numpy as np
import time
start = time.time()
a=0

print('\n')
print('*********************************************************')
print('Metode Binary Search untuk Penyelesaian Economic Dispatch')
print('------- dengan Piecewise Function Characteristic --------')
print('\n')
print('Vincentius Wahyu W')
print('16/399923/TK/44937')

"""
- Inisialisasi Daya Pembangkit, Linear Cost Bahan Bakar,
    Harga Bahan Bakar per MBtu, Permintaan Daya
- Berbeda pembangkit --> Berbeda Row Array
"""

#Insialisasi Fungsi
p = np.array([[100, 200, 300, 400], [150, 275, 390, 450], [130, 260, 430,500],[170,300,450,600]], dtype=np.float64)
#print(p[:,1])
#p = Daya (MW), tiap row menyatakan tiap pembangkit. Tiap Kolom menyatakan tiap breakpoint
ihr = np.array([[7000, 8200, 8900, 11000], [7500, 7700, 8100, 8500],[7300,8300,9000,10000],[7100,8300,8800,10300]], dtype=np.float64)
demand = 1200 #Daya yang ingin dibangkitkan
costUnit = np.array([1.6, 2.1, 1.8, 2.2], dtype=np.float64) #Cost Pembangkitan,
tol = 0.000001

bp = len(ihr[0, :])
nGen = len(ihr[:, 0])

lamda = np.zeros(shape=(nGen, bp))
slope = np.zeros(shape=(nGen, bp))
const = np.zeros(shape=(nGen, bp))
temp_slope = np.ones(shape=(nGen, bp))
temp_constant = np.ones(shape=(nGen, bp))
Pow_max= np.ones(shape=(nGen, 1))
Pow_min= np.ones(shape=(nGen, 1))
Pow= np.ones(shape=(nGen, 1))


#Menghitung Nilai Slope, Constant dari Fungsi Piecewise tiap Segmen
for j in range(nGen):
    for i in range(bp):
        lamda[j, i] = (ihr[j, i] * costUnit[j]) / 1000
for j in range(nGen):
    for i in range(bp - 1):
        slope[j, i + 1] = (lamda[j, i + 1] - lamda[j, i]) / (p[j, i + 1] - p[j, i])
        const[j, i + 1] = lamda[j, i] - (slope[j, i+1] * p[j, i])

#Menghitung Nilai Maksimum dan Minimum Load tiap Pembangkit
for i in range (nGen):
    Pow_max[i,0]=np.amax(p[i,:])
for i in range(nGen):
    Pow_min[i, 0] = np.amin(p[i, :])

#Exit Jika Permintaan Daya di luar Range
if demand < sum(Pow_min):
    print("Daya Pemabangkitan  kurang dari Technical Minimum Load")
    exit()
elif demand > sum(Pow_max):
    print("Daya Pemabangkitan  lebih dari Technical Maximum Load")
    exit()

#Menentukan Nilai lamda
max_lam = np.amax(lamda)
min_lam = np.amin(lamda)
delta_lam = (max_lam - min_lam) / 2
min_lam += delta_lam

#print(lamda)
#Iterasi Binary Search
while 1:
    #Memilih Segmen
    for i in range(nGen):
        if min_lam <= lamda[i, 0]:
            temp_slope[i,0]=slope[i,0]
            temp_constant[i,0]=const[i,0]
        for j in range(bp-1):
            if (min_lam>lamda[i,j]) & (min_lam<=lamda[i,j+1]):
                temp_slope[i, 0] = slope[i, j+1]
                temp_constant[i, 0] = const[i, j+1]
        if min_lam>lamda[i,bp-1]:
            temp_slope[i, 0] = slope[i, bp-1]
            temp_constant[i, 0] = const[i, bp-1]

    for i in range(nGen):
        if temp_slope[i,0]==0:
            Pow[i,0]=Pow_min[i,0]
        elif (min_lam-temp_constant[i,0])/temp_slope[i,0]>=Pow_max[i,0]:
            Pow[i,0]=Pow_max[i,0]
        else:
            Pow[i, 0]=(min_lam-temp_constant[i,0])/temp_slope[i,0]

    if sum(Pow)>demand:
        delta_lam=delta_lam/2
        min_lam-=delta_lam
    else:
        delta_lam = delta_lam / 2
        min_lam += delta_lam

    a+=1
    #print(sum(Pow))
    #print(Pow)
    if abs(sum(Pow)-demand)<= tol:
        break

#Visualiasi Data
#Tabel
for i in range (nGen):
    print('\n')
    print('========================================================')
    print('Pembangkit Unit ',i+1,)
    print('========================================================')
    print('No. \t Segmen \t\t Increment \t\t\t Lamda')
    print('1   \t ',1,' \t\t', lamda[i,0], '\t\t\t\t\t', lamda[i,0])
    for j in range (bp-1):
        print(j+2,'   \t ',j+2,' \t', '%.5f'%slope[i,j+1],'*P +','%.5f'%const[i,j+1],'\t\t', lamda[i,j+1])

print('\n')
print('========================================================')

print('Nilai Lamda \t\t\t:', min_lam)
print('Jumlah Iterasi \t\t\t:', a)
print('Permintaan Beban \t\t:', demand)
for i in range(nGen):
    print('Daya Pembangkit Unit',i+1,'\t:',Pow[i,0])
end = time.time()
print('Waktu Eksekusi', end - start)

#Plot Grafik
plt.figure(1)
for i in range (nGen):
    plt.plot(p[i],lamda[i],label=i+1,)
    plt.scatter(p[i],lamda[i])
plt.grid()
plt.legend(loc='upper left')
#plt.axes.Axes.scatter(min_lam)
plt.title('Incremental Cost')
plt.xlabel('Power (MW)')
plt.ylabel('Cost ($/KWh)')
plt.show()

