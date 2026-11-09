USE `yslteam`;

DROP TABLE IF EXISTS `list_training`;
CREATE TABLE `list_training` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `no` INT NOT NULL,
  `fungsi` VARCHAR(100),
  `id_fungsi` VARCHAR(50),
  `level_posisi` VARCHAR(50),
  `id_level_posisi` VARCHAR(50),
  `level_training` VARCHAR(50),
  `id_level_training` VARCHAR(50),
  `group_posisi` VARCHAR(100),
  `id_group_posisi` VARCHAR(50),
  `kode_training` VARCHAR(50),
  `nama` VARCHAR(150),
  `egi` VARCHAR(50),
  `competency` VARCHAR(150),
  `id_competency_level` VARCHAR(50),
  `status` VARCHAR(50),
  `nama_training` VARCHAR(200),
  `tanggal_mulai` DATE,
  `batch` VARCHAR(50),
  `jumlah_partisipasi` INT,
  `durasi_jam` INT,
  `penyelenggara` VARCHAR(150),
  `lokasi` VARCHAR(100),
  `pic` VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `list_training` (`no`, `fungsi`, `id_fungsi`, `level_posisi`, `id_level_posisi`, `level_training`, `id_level_training`, `group_posisi`, `id_group_posisi`, `kode_training`, `nama`, `egi`, `competency`, `id_competency_level`, `status`, `nama_training`, `tanggal_mulai`, `batch`, `jumlah_partisipasi`, `durasi_jam`, `penyelenggara`, `lokasi`, `pic`) VALUES
(1, 'Manajemen', 'F001', '1', 'L1', 'Teknis', 'T001', 'Staff', 'G001', 'TR001', 'Manajemen Proyek', 'A', 'Leadership', 'C1', 'Aktif', 'Project Management Fundamentals', '2025-05-12', 'B001', 25, 16, 'Lembaga Konsultan', 'Jakarta', 'Budi Santoso'),
(2, 'Teknologi Informasi', 'F002', '2', 'L2', 'Softskill', 'T002', 'Staff IT', 'G002', 'TR002', 'Digital Literacy', 'B', 'Technical Skill', 'C2', 'Aktif', 'Basic Digital Skills', '2025-06-02', 'B002', 12, 12, 'Internal', 'Bandung', 'Sari Wulandari'),
(3, 'Keuangan', 'F003', '1', 'L1', 'Teknis', 'T003', 'Staff', 'G003', 'TR003', 'Akuntansi Dasar', 'A', 'Financial Management', 'C1', 'Pending', 'Financial Accounting for Non Financial', '2025-06-10', 'B003', 16, 16, 'PT. Prima Konsultan', 'Surabaya', 'Andi Setiawan'),
(4, 'HRD', 'F004', '2', 'L2', 'Softskill', 'T004', 'Staff HR', 'G004', 'TR004', 'Komunikasi Efektif', 'B', 'Communication', 'C2', 'Aktif', 'Effective Communication', '2025-06-15', 'B004', 15, 12, 'Lembaga Konsultan', 'Yogyakarta', 'Rina Aprilia'),
(5, 'Pemasaran', 'F005', '1', 'L1', 'Teknis', 'T005', 'Staff', 'G005', 'TR005', 'Digital Marketing', 'A', 'Marketing Skill', 'C1', 'Aktif', 'Social Media Marketing', '2025-07-01', 'B005', 18, 12, 'Eksternal', 'Bali', 'Dewi Lestari'),
(6, 'Operasional', 'F006', '1', 'L1', 'Teknis', 'T006', 'Staff Ops', 'G006', 'TR006', 'Keselamatan Kerja', 'A', 'Safety', 'C1', 'Aktif', 'Workplace Safety Management', '2025-07-10', 'B006', 20, 16, 'PT. Safety Indo', 'Semarang', 'Agus Pratama'),
(7, 'R&D', 'F007', '2', 'L2', 'Softskill', 'T007', 'Staff R&D', 'G007', 'TR007', 'Inovasi dan Kreativitas', 'B', 'Problem Solving', 'C2', 'Pending', 'Creative Thinking Workshop', '2025-07-15', 'B007', 14, 16, 'Internal', 'Bandung', 'Rizky Hidayat'),
(8, 'Legal', 'F008', '1', 'L1', 'Teknis', 'T008', 'Staff Legal', 'G008', 'TR008', 'Hukum Perusahaan', 'A', 'Legal Knowledge', 'C1', 'Aktif', 'Corporate Law Basics', '2025-07-20', 'B008', 10, 14, 'Lembaga Konsultan', 'Jakarta', 'Fajar Ramadhan');