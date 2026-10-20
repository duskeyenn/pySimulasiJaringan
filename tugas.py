import random
import time

IP_ASAL = "10.0.0.1"
IP_TUJUAN = "10.0.0.9"
UKURAN = 4  


def pecah(pesan):
    pesan = pesan.replace(" ", "").upper()
    paket = []
    for i in range(0, len(pesan), UKURAN):
        paket.append({
            "no": len(paket) + 1,
            "asal": IP_ASAL,
            "tujuan": IP_TUJUAN,
            "payload": pesan[i:i + UKURAN],
        })
    return pesan, paket


def cetak_kartu(daftar):
    print(f"{'Paket':<7}{'IP asal':<11}{'IP tujuan':<11}{'No.urut':<9}Payload")
    for p in daftar:
        print(f"{p['no']:<7}{p['asal']:<11}{p['tujuan']:<11}{p['no']:<9}{p['payload']}")


def main():
    pesan_asli = input("Masukkan teks pesan: ")
    pesan, paket = pecah(pesan_asli)
    if len(paket) < 2:
        print("Pesan terlalu pendek, minimal 5 huruf.")
        return

    print(f"\nPesan (tanpa spasi): {pesan} ({len(pesan)} karakter)")
    print(f"\n=== LANGKAH 1: Kartu paket ({len(paket)} paket) ===")
    cetak_kartu(paket)

    mulai = time.time()


    acak = paket[:]
    random.shuffle(acak)
    for p in acak:
        p["jalur"] = random.choice(["R1", "R2"])


    hilang = random.choice(paket)

    tiba = [p for p in acak if p is not hilang]
    print("\n=== LANGKAH 2 & 3: Kirim lewat router, satu paket hilang ===")
    print(f"Paket hilang: nomor {hilang['no']} (payload {hilang['payload']})")

    print("\n=== LANGKAH 4: Penerima menyusun ===")
    urut_tiba = [p["no"] for p in tiba]
    print("Urutan kedatangan paket:", urut_tiba)
    sementara = sorted(tiba, key=lambda p: p["no"])
    teks = ""
    nomor_ada = {p["no"] for p in sementara}
    for p in paket:
        teks += p["payload"] if p["no"] in nomor_ada else "." * len(p["payload"])
    print("Pesan sementara:", teks)
    print(f"Penerima minta kirim ulang paket nomor {hilang['no']}...")
    tiba.append(hilang)
    urut_tiba.append(hilang["no"])
    lengkap = "".join(p["payload"] for p in sorted(tiba, key=lambda p: p["no"]))
    print("Pesan lengkap:", lengkap)
    print("ACK, pesan diterima" if lengkap == pesan else "Pesan belum cocok!")

    total = max(1, round(time.time() - mulai))
    print("\n=== TABEL LOG ===")
    print(f"{'Paket':<7}{'Jalur':<8}{'Urutan tiba':<13}{'Hilang?':<9}Dikirim ulang?")
    for p in paket:
        ya = p is hilang
        print(f"{p['no']:<7}{p['jalur']:<8}{urut_tiba.index(p['no']) + 1:<13}"
              f"{'Ya' if ya else 'Tidak':<9}{'Ya' if ya else 'Tidak'}")

    n = len(paket)
    print("\n=== LANGKAH 5: Perhitungan ===")
    print(f"Paket dikirim (pertama) : {n}")
    print(f"Paket hilang            : 1")
    print(f"Packet loss             : 1/{n} x 100% = {1 / n * 100:.2f}%")
    print("Hop                     : 2 (pengirim -> router -> penerima)")
    print("Total waktu & throughput: isi dari stopwatch asli kamu,")
    print(f"                          throughput = {len(pesan)} karakter / total waktu")


main()

