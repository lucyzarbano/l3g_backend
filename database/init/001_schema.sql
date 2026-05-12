CREATE TABLE rooms (
  id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  description TEXT NOT NULL,
  short_description VARCHAR(500) NOT NULL,
  cover_image_src VARCHAR(500) NOT NULL,
  cover_image_alt VARCHAR(255) NOT NULL,
  link VARCHAR(255) NOT NULL,
  rate DECIMAL(2,1) NOT NULL DEFAULT 0,
  price_base DECIMAL(8,2) NULL,
  capacity TINYINT UNSIGNED NULL,
  visible_in_home BOOLEAN NOT NULL DEFAULT TRUE,
  reverse_layout BOOLEAN NOT NULL DEFAULT FALSE,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE room_images (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  room_id VARCHAR(64) NOT NULL,
  src VARCHAR(500) NOT NULL,
  alt VARCHAR(255) NOT NULL,
  is_cover BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_room_images_room
    FOREIGN KEY (room_id) REFERENCES rooms(id)
    ON DELETE CASCADE
);

CREATE TABLE services (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  icon_key VARCHAR(120) NOT NULL,
  UNIQUE KEY uq_services_name (name)
);

CREATE TABLE room_services (
  room_id VARCHAR(64) NOT NULL,
  service_id BIGINT UNSIGNED NOT NULL,
  service_group ENUM('base', 'additional') NOT NULL DEFAULT 'base',
  sort_order INT NOT NULL DEFAULT 0,
  PRIMARY KEY (room_id, service_id, service_group),
  CONSTRAINT fk_room_services_room
    FOREIGN KEY (room_id) REFERENCES rooms(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_room_services_service
    FOREIGN KEY (service_id) REFERENCES services(id)
    ON DELETE CASCADE
);

CREATE TABLE room_badges (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  room_id VARCHAR(64) NOT NULL,
  label VARCHAR(120) NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_room_badges_room
    FOREIGN KEY (room_id) REFERENCES rooms(id)
    ON DELETE CASCADE
);

CREATE TABLE places (
  id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(160) NOT NULL,
  details_title VARCHAR(220) NOT NULL,
  description TEXT NOT NULL,
  cover_image_src VARCHAR(500) NOT NULL,
  cover_image_alt VARCHAR(255) NOT NULL,
  event_date VARCHAR(80) NULL,
  address VARCHAR(255) NULL,
  distance_km DECIMAL(6,2) NULL,
  category VARCHAR(120) NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE place_images (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  place_id VARCHAR(64) NOT NULL,
  src VARCHAR(500) NOT NULL,
  alt VARCHAR(255) NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_place_images_place
    FOREIGN KEY (place_id) REFERENCES places(id)
    ON DELETE CASCADE
);

CREATE TABLE place_info_items (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  place_id VARCHAR(64) NOT NULL,
  icon_key VARCHAR(120) NOT NULL,
  title VARCHAR(160) NOT NULL,
  type VARCHAR(120) NOT NULL,
  description VARCHAR(255) NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_place_info_items_place
    FOREIGN KEY (place_id) REFERENCES places(id)
    ON DELETE CASCADE
);

CREATE TABLE about_sections (
  id VARCHAR(64) PRIMARY KEY,
  eyebrow VARCHAR(160) NOT NULL,
  title VARCHAR(160) NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order INT NOT NULL DEFAULT 0
);

CREATE TABLE about_paragraphs (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  about_section_id VARCHAR(64) NOT NULL,
  body TEXT NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_about_paragraphs_section
    FOREIGN KEY (about_section_id) REFERENCES about_sections(id)
    ON DELETE CASCADE
);

CREATE TABLE about_images (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  about_section_id VARCHAR(64) NOT NULL,
  src VARCHAR(500) NOT NULL,
  alt VARCHAR(255) NOT NULL,
  class_name VARCHAR(80) NULL,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_about_images_section
    FOREIGN KEY (about_section_id) REFERENCES about_sections(id)
    ON DELETE CASCADE
);
