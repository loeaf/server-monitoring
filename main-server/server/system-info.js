const Sequelize = require('sequelize');

module.exports = (sequelize) => {
  return sequelize.define('system_info', {
    system_name: {
      type: Sequelize.STRING,
      allowNull: false
    },
    total_disk: {
      type: Sequelize.STRING,
      allowNull: false,
      unique: true
    },
    use_disk: {
      type: Sequelize.STRING,
      allowNull: false
    },
    percent_disk: {
      type: Sequelize.STRING,
      allowNull: false,
      unique: true
    },
    use_cpu: {
      type: Sequelize.STRING,
      allowNull: false
    },
    total_mem: {
      type: Sequelize.STRING,
      allowNull: false
    },
    use_mem: {
      type: Sequelize.STRING,
      allowNull: false
    },
    percent_mem: {
      type: Sequelize.STRING,
      allowNull: false
    }
  });
};