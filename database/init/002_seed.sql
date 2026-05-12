INSERT INTO rooms (
  id, title, description, short_description, cover_image_src, cover_image_alt,
  link, rate, price_base, capacity, visible_in_home, reverse_layout, active, sort_order
) VALUES
('ambra', 'Camera Ambra', 'La Camera Ambra prende il nome dall''omonima pietra. La stanza e dotata di letto matrimoniale con la possibilita di aggiungere ulteriori posti letto. E'' provvista di un comodo bagno in camera, l''ambiente e totalmente climatizzato e dotato di riscaldamenti.', 'Spaziosa e accogliente, ideale per chi cerca comfort e tranquillita.', '/src/assets/img/camera_ambra.png', 'Camera Ambra', '/room/ambra', 5.0, 88.00, 3, TRUE, TRUE, TRUE, 1),
('topazio', 'Camera Topazio', 'La Camera Topazio prende il nome dall''omonima pietra. La stanza e dotata di letto matrimoniale con la possibilita di aggiungere ulteriori posti letto. E'' provvista di un comodo bagno in camera, l''ambiente e totalmente climatizzato e dotato di riscaldamenti.', 'Confortevole e luminosa, pensata per un soggiorno pratico e rilassante.', '/src/assets/img/camera_topazio.png', 'Camera Topazio', '/room/topazio', 4.5, 82.00, 2, TRUE, FALSE, TRUE, 2),
('zaffiro', 'Camera Zaffiro', 'La Camera Zaffiro prende il nome dall''omonima pietra. La stanza e dotata di letto matrimoniale con la possibilita di aggiungere ulteriori posti letto. E'' provvista di un comodo bagno in camera, l''ambiente e totalmente climatizzato e dotato di riscaldamenti.', 'Raccolta e piacevole, con affaccio sulla citta e un''atmosfera rilassata.', '/src/assets/img/camera_zaffiro.jpeg', 'Camera Zaffiro', '/room/zaffiro', 3.0, 76.00, 2, TRUE, TRUE, FALSE, 3);

INSERT INTO room_images (room_id, src, alt, is_cover, sort_order) VALUES
('ambra', '/src/assets/img/camera_ambra.png', 'Camera Ambra', TRUE, 1),
('ambra', '/src/assets/img/camere/camera_ambra/camera_ambra_01.jpeg', 'Camera Ambra', FALSE, 2),
('ambra', '/src/assets/img/camere/camera_ambra/camera_ambra_02.jpeg', 'Camera Ambra', FALSE, 3),
('ambra', '/src/assets/img/camere/camera_ambra/camera_ambra_03.jpeg', 'Camera Ambra', FALSE, 4),
('ambra', '/src/assets/img/camere/camera_ambra/camera_ambra_04.jpeg', 'Camera Ambra', FALSE, 5),
('ambra', '/src/assets/img/camere/camera_ambra/camera_ambra_05.jpeg', 'Camera Ambra', FALSE, 6),
('topazio', '/src/assets/img/camera_topazio.png', 'Camera Topazio', TRUE, 1),
('zaffiro', '/src/assets/img/camera_zaffiro.jpeg', 'Camera Zaffiro', TRUE, 1);

INSERT INTO services (name, icon_key) VALUES
('Wifi Gratis', 'faWifi'),
('Vista della citta', 'faCity'),
('Aria Condizionata', 'faTemperatureArrowDown'),
('Balcone', 'faLocationDot'),
('Tv a schermo piatto', 'faTv'),
('Bagno Privato', 'faSink'),
('Parcheggio Privato', 'faSquareParking'),
('5 km dal B&B', 'faWater'),
('Climatizzatore', 'faTemperatureArrowDown');

INSERT INTO room_services (room_id, service_id, service_group, sort_order)
SELECT r.id, s.id, 'base', x.sort_order
FROM rooms r
JOIN (
  SELECT 'ambra' room_id, 'Wifi Gratis' service_name, 1 sort_order UNION ALL
  SELECT 'ambra', 'Vista della citta', 2 UNION ALL
  SELECT 'ambra', 'Aria Condizionata', 3 UNION ALL
  SELECT 'ambra', 'Balcone', 4 UNION ALL
  SELECT 'ambra', 'Tv a schermo piatto', 5 UNION ALL
  SELECT 'ambra', 'Bagno Privato', 6 UNION ALL
  SELECT 'topazio', 'Wifi Gratis', 1 UNION ALL
  SELECT 'topazio', 'Vista della citta', 2 UNION ALL
  SELECT 'topazio', 'Aria Condizionata', 3 UNION ALL
  SELECT 'topazio', 'Balcone', 4 UNION ALL
  SELECT 'topazio', 'Tv a schermo piatto', 5 UNION ALL
  SELECT 'topazio', 'Bagno Privato', 6 UNION ALL
  SELECT 'zaffiro', 'Wifi Gratis', 1 UNION ALL
  SELECT 'zaffiro', 'Vista della citta', 2 UNION ALL
  SELECT 'zaffiro', 'Aria Condizionata', 3 UNION ALL
  SELECT 'zaffiro', 'Balcone', 4
) x ON x.room_id = r.id
JOIN services s ON s.name = x.service_name;

INSERT INTO room_services (room_id, service_id, service_group, sort_order)
SELECT r.id, s.id, 'additional', x.sort_order
FROM rooms r
JOIN (
  SELECT 'ambra' room_id, 'Parcheggio Privato' service_name, 1 sort_order UNION ALL
  SELECT 'ambra', '5 km dal B&B', 2 UNION ALL
  SELECT 'ambra', 'Climatizzatore', 3 UNION ALL
  SELECT 'topazio', 'Parcheggio Privato', 1 UNION ALL
  SELECT 'topazio', '5 km dal B&B', 2 UNION ALL
  SELECT 'topazio', 'Climatizzatore', 3 UNION ALL
  SELECT 'zaffiro', 'Parcheggio Privato', 1 UNION ALL
  SELECT 'zaffiro', '5 km dal B&B', 2 UNION ALL
  SELECT 'zaffiro', 'Climatizzatore', 3
) x ON x.room_id = r.id
JOIN services s ON s.name = x.service_name;

INSERT INTO room_badges (room_id, label, sort_order) VALUES
('ambra', 'Piu comoda', 1),
('topazio', 'Piu venduta', 1),
('zaffiro', 'Piu consigliata', 1);

INSERT INTO places (
  id, title, details_title, description, cover_image_src, cover_image_alt,
  event_date, address, distance_km, category, active, sort_order
) VALUES
('valle-dei-templi', 'Valle dei Templi', 'Area archeologica di Agrigento', 'Uno dei luoghi archeologici piu celebri della Sicilia, perfetto per una giornata tra storia, templi dorici e paesaggi aperti.', 'src/assets/img/01_CHIESA_MADRE.jpg', 'Valle dei templi', '18 Febbraio 2025', 'Agrigento', NULL, 'Cultura', TRUE, 1),
('etna', 'Scopri l''Etna', 'Etna', 'L''Etna e un vulcano attivo e una delle mete piu suggestive della Sicilia orientale. Tra crateri, boschi, grotte e panorami lavici, offre scenari sempre diversi e perfetti per una giornata di esplorazione.', 'src/assets/img/01_ETNA.jpg', 'Etna', '12 Febbraio 2025', 'Parco dell Etna, Catania', 55.00, 'Natura', TRUE, 2),
('lago-lentini', 'Lago di Lentini', 'Lago di Lentini', 'Il lago di Lentini, conosciuto anche come Biviere, e un''oasi naturalistica ideale per chi ama paesaggi tranquilli, birdwatching e scorci aperti a pochi minuti dalla citta.', 'src/assets/img/01_LAGO_LENTINI.jpg', 'Lago di Lentini', '18 Febbraio 2025', 'Contrada Biviere, Lentini', 8.00, 'Natura', TRUE, 3),
('chiesa-madre', 'Chiesa Madre', 'Chiesa di sant''Alfio', 'Edificata tra il 1700 e il 1750 in stile barocco, la Chiesa Madre e uno dei luoghi simbolo del centro storico di Lentini.', 'src/assets/img/01_CHIESA_MADRE.jpg', 'Chiesa Madre di Lentini', '18 Febbraio 2025', 'Piazza Duomo, Lentini', 1.20, 'Cultura', TRUE, 4);

INSERT INTO place_images (place_id, src, alt, sort_order) VALUES
('valle-dei-templi', 'src/assets/img/01_VALLE_DEI_TEMPLI.jpg', 'Valle dei Templi', 1),
('valle-dei-templi', 'src/assets/img/02_VALLE_DEI_TEMPLI.jpg', 'Valle dei Templi', 2),
('etna', 'src/assets/img/01_ETNA.jpg', 'Etna', 1),
('etna', 'src/assets/img/02_ETNA.jpg', 'Etna', 2),
('lago-lentini', 'src/assets/img/01_LAGO_LENTINI.jpg', 'Lago di Lentini', 1),
('lago-lentini', 'src/assets/img/02_LAGO_LENTINI.jpg', 'Lago di Lentini', 2),
('chiesa-madre', 'src/assets/img/01_CHIESA_MADRE.jpg', 'Chiesa Madre', 1),
('chiesa-madre', 'src/assets/img/02_CHIESA_MADRE.jpg', 'Chiesa Madre', 2);

INSERT INTO place_info_items (place_id, icon_key, title, type, description, sort_order) VALUES
('valle-dei-templi', 'faLocationDot', 'Distanza dal B&B', 'Chiesa', '5 km / 10 min a piedi', 1),
('valle-dei-templi', 'faTag', 'Tipo di Luogo', 'Lago', '6 km / 12 min in auto', 2),
('valle-dei-templi', 'faClock', 'Percorrenza', '2 ore in auto', '15 km / 30 min in auto', 3),
('etna', 'faLocationDot', 'Distanza dal B&B', 'Chiesa', '5 km / 10 min a piedi', 1),
('etna', 'faTag', 'Tipo di Luogo', 'Lago', '6 km / 12 min in auto', 2),
('etna', 'faClock', 'Percorrenza', '2 ore in auto', '15 km / 30 min in auto', 3),
('lago-lentini', 'faLocationDot', 'Distanza dal B&B', 'Chiesa', '5 km / 10 min a piedi', 1),
('lago-lentini', 'faTag', 'Tipo di Luogo', 'Lago', '6 km / 12 min in auto', 2),
('lago-lentini', 'faClock', 'Percorrenza', '2 ore in auto', '15 km / 30 min in auto', 3),
('chiesa-madre', 'faLocationDot', 'Distanza dal B&B', 'Chiesa', '5 km / 10 min a piedi', 1),
('chiesa-madre', 'faTag', 'Tipo di Luogo', 'Lago', '6 km / 12 min in auto', 2),
('chiesa-madre', 'faClock', 'Percorrenza', '2 ore in auto', '15 km / 30 min in auto', 3);

INSERT INTO about_sections (id, eyebrow, title, active, sort_order) VALUES
('home-about', 'Nel cuore di Lentini', 'Chi Siamo', TRUE, 1);

INSERT INTO about_paragraphs (about_section_id, body, sort_order) VALUES
('home-about', 'Il B&B Le Tre Gemme si trova in via Conte Alaimo, nel centro storico di Lentini, in provincia di Siracusa.', 1),
('home-about', 'A pochi passi dalla struttura puoi riscoprire la bellezza, la cultura e la storia del paese, dalla chiesa di San Francesco di Paola alla chiesa madre di Sant''Alfio, preziosa testimonianza del barocco siciliano.', 2),
('home-about', 'Lentini e una base ideale per visitare la Sicilia orientale: il mare dista 10 km, Catania 25 km, Siracusa 45 km, mentre Etna, Noto e Taormina sono facilmente raggiungibili per una giornata speciale.', 3),
('home-about', 'Le Tre Gemme offre un soggiorno confortevole in un ambiente ospitale, curato e accogliente.', 4);

INSERT INTO about_images (about_section_id, src, alt, class_name, sort_order) VALUES
('home-about', '/src/assets/img/chi-siamo_1.jpg', 'Dettaglio accogliente del B&B Le Tre Gemme', 'img_1', 1),
('home-about', '/src/assets/img/chi-siamo_2.jpg', 'Ambiente luminoso del B&B Le Tre Gemme', 'img_2', 2);
