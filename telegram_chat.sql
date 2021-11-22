-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Ноя 20 2021 г., 20:19
-- Версия сервера: 10.3.31-MariaDB-0ubuntu0.20.04.1
-- Версия PHP: 7.4.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `telegram_chat`
--

-- --------------------------------------------------------

--
-- Структура таблицы `awaiting`
--

CREATE TABLE `awaiting` (
  `id` int(10) NOT NULL,
  `chat_id` int(10) NOT NULL,
  `msg_id` int(11) NOT NULL,
  `sex` int(11) NOT NULL DEFAULT 0,
  `prefer_sex` int(11) NOT NULL DEFAULT 0,
  `wait_time` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `banlist`
--

CREATE TABLE `banlist` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `bandate` datetime NOT NULL DEFAULT current_timestamp(),
  `reason` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `complains`
--

CREATE TABLE `complains` (
  `id` int(11) NOT NULL,
  `plf_id` int(11) NOT NULL,
  `def_id` int(11) NOT NULL,
  `timee` timestamp NOT NULL DEFAULT current_timestamp(),
  `time2` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `current_dialogs`
--

CREATE TABLE `current_dialogs` (
  `id` int(11) NOT NULL,
  `chat_id1` int(11) NOT NULL,
  `chat_id2` int(11) NOT NULL,
  `last_msg1` int(11) NOT NULL DEFAULT 0,
  `last_msg2` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `messages`
--

CREATE TABLE `messages` (
  `id` int(10) UNSIGNED NOT NULL,
  `id_sender` int(10) UNSIGNED NOT NULL,
  `id_recipient` int(10) UNSIGNED NOT NULL,
  `added_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `msg_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `settings`
--

CREATE TABLE `settings` (
  `id` int(11) NOT NULL,
  `setting` text DEFAULT NULL,
  `set_int` int(11) NOT NULL DEFAULT 0,
  `set_text` text DEFAULT NULL,
  `set_bool` tinyint(1) NOT NULL DEFAULT 0,
  `set_text2` text DEFAULT NULL,
  `set_int2` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `f_name` text NOT NULL,
  `l_name` text NOT NULL,
  `chat_id` int(11) NOT NULL,
  `username` text NOT NULL,
  `age` int(11) NOT NULL DEFAULT 0,
  `sex` int(11) NOT NULL DEFAULT 0,
  `rating` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `users_start`
--

CREATE TABLE `users_start` (
  `id` int(11) NOT NULL,
  `chat_id` int(11) NOT NULL DEFAULT 0,
  `f_name` text NOT NULL,
  `newuser` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `users_vip`
--

CREATE TABLE `users_vip` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `awaiting`
--
ALTER TABLE `awaiting`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `banlist`
--
ALTER TABLE `banlist`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `complains`
--
ALTER TABLE `complains`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `current_dialogs`
--
ALTER TABLE `current_dialogs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `filter` (`id_sender`,`id_recipient`);

--
-- Индексы таблицы `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users_start`
--
ALTER TABLE `users_start`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users_vip`
--
ALTER TABLE `users_vip`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `awaiting`
--
ALTER TABLE `awaiting`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `banlist`
--
ALTER TABLE `banlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `complains`
--
ALTER TABLE `complains`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `settings`
--
ALTER TABLE `settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `users_start`
--
ALTER TABLE `users_start`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `users_vip`
--
ALTER TABLE `users_vip`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
