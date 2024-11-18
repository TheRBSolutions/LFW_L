const growRate = 10
let newUsers = 0
const sessions = {}
let lastIndex = 0
const maxRounds = 1000

function updateGraph () {
  const keys = Object.keys(sessions)
  const p = random(100)
  const row = new Row(keys.length, p)
  keys.forEach(sessionId => {
    const session = sessions[sessionId]
    const action = session.user.run(random(100))
    switch (action) {
      case 'ACTION':
        row.actions++
        break
      case 'LOGOFF':
        row.logoffs++
        delete sessions[sessionId]
        break
    }
    if (action === '') {
      session.timeout--
    } else {
      session.timeout = 3
    }
    if (session.timeout === 0) {
      row.logoffs++
      delete sessions[sessionId]
    }
  })
  const nUsers = randomSign() * random(growRate)
  newUsers = nUsers + newUsers < 0 ? 0 : nUsers + newUsers
  createUsers(newUsers, sessions, lastIndex)
  lastIndex += newUsers
  row.logins = newUsers
  row.total = row.total + row.logins - row.logoffs
  return row
}

document.addEventListener('DOMContentLoaded', (event) => {
  console.log(event.type)
  const labels = [0]
  const ctx = document.getElementById('web').getContext('2d')
  const config = createConfigGraph(labels)
  const g = createGraph(ctx, config)
  let round = 0
  const id = setInterval(function (e) {
    if (++round >= maxRounds) {
      clearInterval(id)
    }
    const row = updateGraph()
    console.log(row)
    if (g.data.labels.length === 20) {
      g.data.labels.shift()
    }
    console.log(g.data.labels)
    g.data.labels.push(round)
    g.data.datasets.forEach((dataset) => {
      if (dataset.data.length === 20) {
        dataset.data.shift()
      }
      switch (dataset.label) {
        case 'Login':
          dataset.data.push(row.logins)
          break
        case 'Logoff':
          dataset.data.push(-row.logoffs)
          break
        case 'Active':
          dataset.data.push(row.actions)
          break
        case 'Online':
          dataset.data.push(row.total - row.logins - row.actions)
          break
      }
    })
    g.update()
  }, 1000)
})

function createConfigGraph (labels) {
  const dataConfig = {
    labels: labels,
    datasets: [
      createDataSet('Logoff', '0, 200, 125, 0.5'),
      createDataSet('Login', '128, 200, 0, 0.5'),
      createDataSet('Active', '0, 0, 128, 0.5', '-1'),
      createDataSet('Online', '120, 120, 120, 0.5', '-1')
    ]
  }
  const optionsConfig = {
    tooltips: {
      mode: 'index',
      intersect: false
    },
    scales: {
      xAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Round'
        }
      }],
      yAxes: [{
        stacked: true,
        scaleLabel: {
          display: true,
          labelString: 'Users'
        },
        ticks: {
          min: -40,
          max: 300
        }
      }]
    }
  }
  const config = {
    type: 'line',
    data: dataConfig,
    options: optionsConfig
  }
  return config
  function createDataSet (name, color, fillMode) {
    return {
      label: name,
      data: [0],
      borderColor: `rgba(${color})`,
      backgroundColor: `rgba(${color})`,
      fill: fillMode
    }
  }
}

function createGraph (ctx, config) {
  const graph = new Chart(ctx, config)
  return graph
}

function random (n) {
  return Math.floor(Math.random() * n)
}

function randomSign () {
  return Math.random() < 0.5 ? -1 : 1
}

class User {
  constructor (id) {
    this.id = id
    this.logoffs = 5 + random(15)
    this.action = 25 + random(20)
  }
  run (p) {
    let command = ''
    if (p < this.action) {
      command = 'ACTION'
    } else if (p < this.logoffs) {
      command = 'LOGOFF'
    }
    return command
  }
}

function Row (total, probality) {
  this.logins = 0
  this.actions = 0
  this.logoffs = 0
  this.probality = probality
  this.total = total
  this.print = function () {
    console.log(`${pad(this.probality)}: ${pad(this.logins)} ${pad(this.actions)} ${pad(this.logoffs)} ${pad(this.total)}`)
  }
}

function pad (n) {
  return ' '.repeat(8 - String(n).length) + n
}

function createUsers (n, sessions, lastIndex) {
  for (let i = 0; i < n; i++) {
    const user = new User(++lastIndex)
    sessions[lastIndex] = {user: user, timeout: 3}
  }
}

