-- ============================================================
-- YSLTEAM IPD System — Seed Data (Data Awal / Simulasi)
-- Jalankan SETELAH schema.sql
-- ============================================================

USE `yslteam`;

-- User accounts (password plain text untuk testing)
-- TODO: Ganti password dengan hash sebelum production
INSERT INTO `user` (`username`, `password`, `user_name`, `role`) VALUES
('admin',  'admin123',  'Administrator HCD', 'HCD'),
('viewer', 'viewer123', 'Staff Viewer',       'VIEWER');

-- Master Repository Training
INSERT INTO `training_repository`
  (`kode_training`, `nama_training`, `fungsi`, `id_fungsi`,
   `level_posisi`, `id_level_posisi`, `level_training`, `id_level_training`,
   `group_posisi`, `id_group_posisi`, `egi`, `competency`, `id_competency_level`)
VALUES
  ('TR001', 'Project Management Fundamentals',      'Manajemen',          'F001', '1', 'L1', 'Teknis',   'T001', 'Staff',      'G001', 'A', 'Leadership',         'C1'),
  ('TR002', 'Basic Digital Skills',                 'Teknologi Informasi', 'F002', '2', 'L2', 'Softskill','T002', 'Staff IT',   'G002', 'B', 'Technical Skill',    'C2'),
  ('TR003', 'Financial Accounting for Non Financial','Keuangan',           'F003', '1', 'L1', 'Teknis',   'T003', 'Staff',      'G003', 'A', 'Financial Management','C1'),
  ('TR004', 'Effective Communication',              'HRD',                'F004', '2', 'L2', 'Softskill','T004', 'Staff HR',   'G004', 'B', 'Communication',      'C2'),
  ('TR005', 'Social Media Marketing',               'Pemasaran',          'F005', '1', 'L1', 'Teknis',   'T005', 'Staff',      'G005', 'A', 'Marketing Skill',    'C1'),
  ('TR006', 'Workplace Safety Management',          'Operasional',        'F006', '1', 'L1', 'Teknis',   'T006', 'Staff Ops',  'G006', 'A', 'Safety',             'C1'),
  ('TR007', 'Creative Thinking Workshop',           'R&D',                'F007', '2', 'L2', 'Softskill','T007', 'Staff R&D',  'G007', 'B', 'Problem Solving',    'C2'),
  ('TR008', 'Corporate Law Basics',                 'Legal',              'F008', '1', 'L1', 'Teknis',   'T008', 'Staff Legal','G008', 'A', 'Legal Knowledge',    'C1');

-- COE Schedule Data
INSERT INTO `coe_schedule`
  (`kode_training`, `batch`, `status_coe`,
   `tgl_rencana_mulai`, `tgl_rencana_selesai`,
   `tgl_realisasi_mulai`, `tgl_realisasi_selesai`,
   `jumlah_partisipan`, `durasi_jam`, `penyelenggara`, `lokasi`, `pic`)
VALUES
  -- TR001: Batch selesai tepat waktu (Sesuai)
  ('TR001', 'B001', 'Selesai',  '2026-05-12', '2026-05-14', '2026-05-12', '2026-05-14', 25, 16, 'Lembaga Konsultan', 'Jakarta',    'Budi Santoso'),
  -- TR001: Batch sedang berjalan (Belum Realisasi)
  ('TR001', 'B002', 'Aktif',    '2026-10-01', '2026-10-03', NULL,         NULL,          20, 16, 'Lembaga Konsultan', 'Jakarta',    'Budi Santoso'),
  -- TR002: Selesai tapi jadwal bergeser (Tidak Sesuai)
  ('TR002', 'B001', 'Selesai',  '2026-06-02', '2026-06-03', '2026-06-10', '2026-06-11', 12, 12, 'Internal',          'Bandung',    'Sari Wulandari'),
  -- TR003: Belum mulai
  ('TR003', 'B001', 'Pending',  '2026-11-10', '2026-11-12', NULL,         NULL,          16, 16, 'PT. Prima Konsultan','Surabaya',  'Andi Setiawan'),
  -- TR004: Aktif
  ('TR004', 'B001', 'Aktif',    '2026-10-15', '2026-10-16', NULL,         NULL,          15, 12, 'Lembaga Konsultan', 'Yogyakarta', 'Rina Aprilia'),
  -- TR005: Selesai tepat waktu
  ('TR005', 'B001', 'Selesai',  '2026-07-01', '2026-07-02', '2026-07-01', '2026-07-02', 18, 12, 'Eksternal',         'Bali',       'Dewi Lestari'),
  -- TR006: Pending
  ('TR006', 'B001', 'Pending',  '2026-12-01', '2026-12-03', NULL,         NULL,          20, 16, 'PT. Safety Indo',   'Semarang',   'Agus Pratama'),
  -- TR007: Selesai tepat waktu
  ('TR007', 'B001', 'Selesai',  '2026-08-05', '2026-08-06', '2026-08-05', '2026-08-06', 14, 16, 'Internal',          'Bandung',    'Rizky Hidayat');
