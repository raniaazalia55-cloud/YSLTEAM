-- ============================================================
-- YSLTEAM IPD System — Database Schema (DDL)
-- Versi: 2.0 | Tersinkronisasi dengan app.py
-- ============================================================
-- Jalankan file ini untuk membuat struktur database dari awal.
-- Lanjutkan dengan seed.sql untuk data awal.
-- ============================================================

CREATE DATABASE IF NOT EXISTS `yslteam`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `yslteam`;

-- ------------------------------------------------------------
-- Tabel: user
-- Menyimpan akun pengguna sistem IPD
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `coe_schedule`;
DROP TABLE IF EXISTS `training_repository`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id`         INT AUTO_INCREMENT PRIMARY KEY,
  `username`   VARCHAR(50)  UNIQUE NOT NULL,
  `password`   VARCHAR(255) NOT NULL COMMENT 'TODO: Ganti dengan password_hash (werkzeug)',
  `user_name`  VARCHAR(100),
  `role`       ENUM('HCD', 'VIEWER') NOT NULL DEFAULT 'VIEWER',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- Tabel: training_repository
-- Master katalog judul training perusahaan
-- ------------------------------------------------------------
CREATE TABLE `training_repository` (
  `kode_training`       VARCHAR(50)  PRIMARY KEY,
  `nama_training`       VARCHAR(200) NOT NULL,
  `fungsi`              VARCHAR(100),
  `id_fungsi`           VARCHAR(50),
  `level_posisi`        VARCHAR(50),
  `id_level_posisi`     VARCHAR(50),
  `level_training`      VARCHAR(50),
  `id_level_training`   VARCHAR(50),
  `group_posisi`        VARCHAR(100),
  `id_group_posisi`     VARCHAR(50),
  `egi`                 VARCHAR(50),
  `competency`          VARCHAR(150),
  `id_competency_level` VARCHAR(50),
  `created_at`          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- Tabel: coe_schedule
-- Jadwal dan realisasi pelaksanaan training (COE)
-- Foreign key ke training_repository dengan CASCADE DELETE
-- ------------------------------------------------------------
CREATE TABLE `coe_schedule` (
  `id_coe`                INT AUTO_INCREMENT PRIMARY KEY,
  `kode_training`         VARCHAR(50) NOT NULL,
  `batch`                 VARCHAR(50),
  `status_coe`            ENUM('Pending', 'Aktif', 'Selesai') DEFAULT 'Pending',
  `tgl_rencana_mulai`     DATE,
  `tgl_rencana_selesai`   DATE,
  `tgl_realisasi_mulai`   DATE,
  `tgl_realisasi_selesai` DATE,
  `jumlah_partisipan`     INT DEFAULT 0,
  `durasi_jam`            INT DEFAULT 0,
  `penyelenggara`         VARCHAR(150),
  `lokasi`                VARCHAR(100),
  `pic`                   VARCHAR(100),
  `created_at`            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`kode_training`)
      REFERENCES `training_repository`(`kode_training`)
      ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
