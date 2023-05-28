// create server
const express = require('express');
const Sequelize = require('sequelize');

const app = express();
const port = 3000;

// db 연결 및 콘피그 셋팅
const sequelize = require('./db-conn');
// User 모델을 불러옵니다.
const SystemInfo = require('./system-info')(sequelize);
sequelize.sync().then(() => {
  console.log('테이블 싱크가 되었습니다.');
}).catch(err => {
  console.error('테이블 생성에 실패했습니다.', err);
});


// 미들웨어로 오류 처리 핸들러를 등록합니다.
app.use((err, req, res, next) => {
  console.error(err); // 에러를 콘솔에 출력하거나 로그에 기록합니다.
  res.status(500).send('서버 오류'); // 사용자에게 500 오류 응답을 보냅니다.
});

/**
 * 모든 서버 정보에 대하여 조회한다.
 */
app.get('/', (req, res) => {
  // get reqeust param by system_name
  const system_name = req.query.system_name;

  // Prepare the where clause based on the presence of system_name
  const whereClause = system_name ? { system_name } : {};

  // if you want to get all system info, you can use findAll()
  SystemInfo.findAll({
    where: whereClause
  }).then((result) => {
    res.send(result);
  }).catch((err) => {
    console.error(err);
    next(err); // 다음 오류 처리 미들웨어로 이동합니다.
  })
});

/**
 * 서버 정보를 등록한다.
 */
app.get('/monitoring/regist', (req, res) => {
  // get request param
  const system_name = req.query.system_name;
  const total_disk = req.query.total_disk;
  const use_disk = req.query.use_disk;
  const percent_disk = req.query.percent_disk;
  const use_cpu = req.query.use_cpu;
  const total_mem = req.query.total_mem;
  const use_mem = req.query.use_mem;
  const percent_mem = req.query.percent_mem;

  SystemInfo.create({
    system_name: system_name,
    total_disk: total_disk,
    use_disk: use_disk,
    percent_disk: percent_disk,
    use_cpu: use_cpu,
    total_mem: total_mem,
    use_mem: use_mem,
    percent_mem: percent_mem
  }).then((result) => {
    res.send(result);
  }).catch((err) => {
    console.error(err);
    next(err);
  });
});

// listen to port 3000 by default
app.listen(port, () => {
  console.log(`Express app listening at http://localhost:${port}`);
});