
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE DATABASE `discord`;
USE `discord`;
--
-- 資料庫： `discord`
--

-- --------------------------------------------------------

--
-- 資料表結構 `choose`
--

CREATE TABLE `choose` (
  `uId` varchar(50) NOT NULL,
  `mId` int(11) NOT NULL,
  `choose` enum('accept','reject') NOT NULL,
  `reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `choose`
--


-- --------------------------------------------------------

--
-- 資料表結構 `form`
--

CREATE TABLE `form` (
  `fId` int(11) NOT NULL,
  `hostId` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `form`
--


-- --------------------------------------------------------

--
-- 資料表結構 `jobs`
--

CREATE TABLE `jobs` (
  `jId` int(11) NOT NULL,
  `s_time` datetime NOT NULL,
  `deadline` datetime NOT NULL,
  `content` text NOT NULL,
  `pre_time` datetime NOT NULL,
  `status` text NOT NULL,
  `hostId` varchar(50) NOT NULL,
  `clientId` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `jobs`
--

-- --------------------------------------------------------

--
-- 資料表結構 `meeting`
--

CREATE TABLE `meeting` (
  `mId` int(11) NOT NULL,
  `s_time` datetime NOT NULL,
  `location` text NOT NULL,
  `content` text NOT NULL,
  `hostId` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `meeting`
--

-- --------------------------------------------------------

--
-- 資料表結構 `tag`
--

CREATE TABLE `tag` (
  `hostId` varchar(50) NOT NULL,
  `clientId` varchar(50) NOT NULL,
  `msgId` varchar(50) NOT NULL,
  `reply` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `tag`
--

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `uId` varchar(50) NOT NULL,
  `status` enum('idle','busy','meeting','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `user`
--


-- --------------------------------------------------------

--
-- 資料表結構 `user_form`
--

CREATE TABLE `user_form` (
  `clientId` varchar(50) NOT NULL,
  `formId` int(11) NOT NULL,
  `food` text NOT NULL,
  `num` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `remark` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `user_form`
--

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `choose`
--
ALTER TABLE `choose`
  ADD PRIMARY KEY (`uId`,`mId`),
  ADD KEY `choose_meetingFK` (`mId`);

--
-- 資料表索引 `form`
--
ALTER TABLE `form`
  ADD PRIMARY KEY (`fId`);

--
-- 資料表索引 `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`jId`);

--
-- 資料表索引 `meeting`
--
ALTER TABLE `meeting`
  ADD PRIMARY KEY (`mId`),
  ADD KEY `meeting_userFK` (`hostId`);

--
-- 資料表索引 `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`hostId`,`clientId`,`msgId`),
  ADD KEY `tag_clientFK` (`clientId`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`uId`);

--
-- 資料表索引 `user_form`
--
ALTER TABLE `user_form`
  ADD PRIMARY KEY (`clientId`,`formId`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `form`
--
ALTER TABLE `form`
  MODIFY `fId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `jobs`
--
ALTER TABLE `jobs`
  MODIFY `jId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `meeting`
--
ALTER TABLE `meeting`
  MODIFY `mId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `choose`
--
ALTER TABLE `choose`
  ADD CONSTRAINT `choose_meetingFK` FOREIGN KEY (`mId`) REFERENCES `meeting` (`mId`);

--
-- 資料表的限制式 `meeting`
--
ALTER TABLE `meeting`
  ADD CONSTRAINT `meeting_userFK` FOREIGN KEY (`hostId`) REFERENCES `user` (`uId`);

--
-- 資料表的限制式 `tag`
--
ALTER TABLE `tag`
  ADD CONSTRAINT `tag_clientFK` FOREIGN KEY (`clientId`) REFERENCES `user` (`uId`),
  ADD CONSTRAINT `tag_hostFK` FOREIGN KEY (`hostId`) REFERENCES `user` (`uId`);
COMMIT;
