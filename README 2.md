LAPORAN ANALISIS PRAKTIKUM
1. Business Question
   - Siapa pelanggan paling royal selama penjualan?
   - Bagaimana flow dari anggaran iklan, efektif ataupun tidak?
   - Bagaimana menanangani produk yang kurang efektif untuk dipejualbelikan?

2. Data Wrangling
   - Merging: Menggabungkan dataset orders, order_items, dan customers menggunakan kunci order_id dan customer_id.
   - Formatting: Mengonversi kolom order_purchase_timestamp menjadi tipe data datetime untuk menghitung metrik waktu.
   - Feature Engineering: * Membuat kolom Total_Sales (hasil penjumlahan price dan freight_value).
   - RFM: Menghitung selisih hari dari transaksi terakhir (Recency), jumlah pesanan per pelanggan (Frequency), dan total pengeluaran (Monetary).
  
3. Insight
   - RFM Analysis (Bar Chart/Table):
     Mayoritas pelanggan berada di segmen Frequency=1 (beli satu kali). Namun, segmen dengan RFM_Group tinggi (seperti 414) menunjukkan potensi pelanggan "baru" yang langsung belanja dalam jumlah besar.

   - Kategori Efisiensi (Horizontal Bar Chart):
     Kategori seperti casa_conforto_2 dan flores muncul sebagai kategori paling tidak efisien. Ini menunjukkan bahwa biaya operasional di kategori tersebut tidak sebanding dengan volume penjualannya.

   - Regresi & Prediksi (Scatter Plot):
     Terdapat korelasi positif yang kuat secara rata-rata (Koefisien: 5.72). Artinya, setiap investasi tambahan pada biaya operasional/iklan terbukti mendongkrak penjualan hingga 5 kali lipat lebih.
