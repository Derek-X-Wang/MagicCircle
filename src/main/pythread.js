const path = require('path')


/*************************************************************
 * py process
 *************************************************************/

const PY_DIST_FOLDER = '../../old/pycalcdist'
const PY_FOLDER = '../../old/pycalc'
const PY_MODULE = 'api' // without .py suffix

let pyProc = null
let pyPort = null

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

const selectPort = () => {
  pyPort = 4242
  return pyPort
}

export const createPyProc = () => {
  let script = getScriptPath()
  let port = '' + selectPort()

  if (guessPackaged()) {
    pyProc = require('child_process').execFile(script, [port])
    console.log("execFile")
  } else {
    pyProc = require('child_process').spawn('python', [script, port])
    pyProc.stderr.on('data', function(data) {
        console.log(data.toString()); 
    });
    console.log("spawn "+script)
  }
 
  if (pyProc != null) {
    //console.log(pyProc)
    console.log('child process success on port ' + port)
  }
}

export const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}
