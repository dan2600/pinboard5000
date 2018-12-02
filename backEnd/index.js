var express = require("express")
const sqlite3 = require('sqlite3').verbose()
var app = express()
var cors = require('cors')
const fileUpload = require('express-fileupload');
const fs = require('fs');

app.use(cors())
app.use(express.json());
app.use(fileUpload({ safeFileNames: true, preserveExtension: true }));
app.use(express.static('public'))

function dbConnect() {
    let db = new sqlite3.Database('./db/pinboard.db', sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
            console.error(err.message)
        }
    })
    return db
}

app.post('/api/imageupload', function(req, res) {
    if (Object.keys(req.files).length == 0) {
        return res.status(400).send('No files were uploaded.');
    }

    // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
    let sampleFile = req.files.file;


    // Use the mv() method to place the file somewhere on your server
    sampleFile.mv('./public/images/' + sampleFile.name, function(err) {
        if (err) { return res.status(500).send(err) }
        let db = dbConnect()
        db.serialize(function() {
            let sql = "DELETE FROM imagelist"
            db.run(sql, undefined, function(err) {
                if (err) {
                    return console.error(err.message);
                }
            })
            sql = "DELETE FROM sqlite_sequence where name='imagelist'"
            db.run(sql, undefined, function(err) {
                if (err) {
                    return console.error(err.message);
                }
            })


            fs.readdirSync('./public/images/').forEach(file => {
                let sql2 = 'INSERT OR IGNORE INTO imagelist (name) VALUES ("' + file + '");'
                db.run(sql2, undefined, function(err) {
                    if (err) {
                        return console.error(err.message);
                    }
                })
            })

            sql = `SELECT * FROM imagelist ORDER BY id`

            db.all(sql, [], (err, rows) => {
                if (err) {
                    throw err
                }
                res.setHeader('Content-Type', 'application/json')
                res.send(JSON.stringify(rows))
                db.close()
            })

        })
    })
})

app.get('/api/playlist', function(req, res) {
    let db = dbConnect()
    let sql = `SELECT * FROM playlist ORDER BY id`
    res.setHeader('Content-Type', 'application/json')
    db.all(sql, [], (err, rows) => {
        if (err) {
            throw err
        }
        res.send(JSON.stringify(rows))
        db.close()
    })
})

app.get('/api/images', function(req, res) {
    let db = dbConnect()
    var sql = `SELECT * FROM imagelist ORDER BY id`
    res.setHeader('Content-Type', 'application/json')
    db.all(sql, [], (err, rows) => {
        if (err) {
            throw err
        }
        res.send(JSON.stringify(rows))
        db.close()
    })
})

app.get('/api/scene/delete', function(req, res) {
    let db = dbConnect()
    let graphicName = req.query.name
    if (!graphicName) {
        return res.send("ERROR")
    } else {
        db.serialize(function() {
            sql = "DELETE FROM scenes WHERE name ='" + graphicName + "'"
            db.run(sql, undefined, function(err) {
                if (err) {
                    return console.error(err.message);
                }
            })
            let sql2 = `SELECT name, imageFile FROM scenes ORDER BY id`
            res.setHeader('Content-Type', 'application/json')
            db.all(sql2, [], (err, rows) => {
                if (err) {
                    throw err
                }
                res.send(JSON.stringify(rows))
                db.close()
            })

        })
    }
})

app.get('/api/deleteImage', function(req, res) {
    let db = dbConnect()
    let graphicName = req.query.name
    if (!graphicName) {
        return res.send("ERROR")
    } else {
        fs.unlink('./public/images/' + graphicName, function() {

            res.setHeader('Content-Type', 'application/json')
            db.serialize(function() {
                sql = "DELETE FROM imagelist"
                db.run(sql, undefined, function(err) {
                    if (err) {
                        return console.error(err.message);
                    }
                })
                sql = "DELETE FROM sqlite_sequence where name='imagelist'"
                db.run(sql, undefined, function(err) {
                    if (err) {
                        return console.error(err.message);
                    }
                })

                fs.readdirSync('./public/images/').forEach(file => {
                    let sql2 = 'INSERT OR IGNORE INTO imagelist (name) VALUES ("' + file + '");'
                    db.run(sql2, undefined, function(err) {
                        if (err) {
                            return console.error(err.message);
                        }
                    })
                })


                sql = `SELECT * FROM imagelist ORDER BY id`
                res.setHeader('Content-Type', 'application/json')
                db.all(sql, [], (err, rows) => {
                    if (err) {
                        throw err
                    }
                    res.send(JSON.stringify(rows))
                    db.close()
                })
            })
        })
    }
})
app.get('/api/scene', function(req, res) {
    let db = dbConnect()
    let graphicName = req.query.name
    if (!graphicName) {
        var sql = `SELECT name, imageFile FROM scenes ORDER BY id`
    } else {
        var sql = `SELECT * FROM scenes WHERE name = '` + graphicName + `' LIMIT 1`
    }
    res.setHeader('Content-Type', 'application/json')
    db.all(sql, [], (err, rows) => {
        if (err) {
            throw err
        }
        res.send(JSON.stringify(rows))
        db.close()
    })
})

app.post('/api/scene/update', function(req, res) {
    let db = dbConnect()
    let data = JSON.parse(req.body.data)
    let entries = data.length
    if (data.id == 999999 || !data.id) {
        var sql3 = `INSERT INTO scenes(name,type,imageFile,frameRate,holdFrame,loopIn,loopOut,loops,font,fontSize,timeX,timeY,tempX,tempY,scrollText,scrollSpeed,colorText,colorBg,blink,blinkSpeed,pinDisplay) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
        var values = [data.name, data.type, data.imageFile, data.frameRate, data.holdFrame, data.loopIn, data.loopOut, data.loops, data.font, data.fontSize, data.timeX, data.timeY, data.tempX, data.tempY, data.scrollText, data.scrollSpeed, data.colorText, data.colorBg, data.blink, data.blinkSpeed, data.pinDisplay]
    } else {
        var sql3 = `UPDATE scenes SET name=?, type=?, imageFile=?, frameRate=?, holdFrame=?,loopIn=?,loopOut=?,loops=?,font=?,fontSize=?,timeX=?,timeY=?,tempX=?,tempY=?,scrollText=?,scrollSpeed=?,colorText=?,colorBG=?,blink=?,blinkSpeed=?,pinDisplay=? WHERE id=?`
        var values = [data.name, data.type, data.imageFile, data.frameRate, data.holdFrame, data.loopIn, data.loopOut, data.loops, data.font, data.fontSize, data.timeX, data.timeY, data.tempX, data.tempY, data.scrollText, data.scrollSpeed, data.colorText, data.colorBg, data.blink, data.blinkSpeed, data.pinDisplay, data.id]
    }

    db.run(sql3, values, function(err) {
        if (err) {
            return console.error(err.message);
        }

    })

    var sql = `SELECT name, imageFile FROM scenes ORDER BY id`
    db.all(sql, [], (err, rows) => {
        if (err) {
            throw err
        }
        res.setHeader('Content-Type', 'application/json')
        res.send(JSON.stringify(rows))
        db.close()
    })
})

app.post('/api/playlist/update', function(req, res) {

    let db = dbConnect()
    let data = JSON.parse(req.body.data)
    let entries = data.length
    let sql = "DELETE FROM playlist WHERE id >= " + entries

    db.serialize(function() {
        db.run(sql, undefined, function(err) {
            if (err) {
                return console.error(err.message);
            }

        })
        for (i = 0; i < entries; i++) {
            let sql3 = 'UPDATE playlist SET graphic="' + data[i].graphic + '" WHERE id=' + i
            let sql2 = 'INSERT OR IGNORE INTO playlist (id, graphic) VALUES (' + i + ',"' + data[i].graphic + '");'
            db.run(sql3, undefined, function(err) {
                if (err) {
                    return console.error("sql3" + err.message);
                }

            })
            db.run(sql2, undefined, function(err) {
                if (err) {
                    return console.error("sql2" + err.message);
                }
            })
        }
        let sql22 = `SELECT * FROM playlist ORDER BY id`
        res.setHeader('Content-Type', 'application/json')
        db.all(sql22, undefined, (err, rows) => {
            if (err) {
                throw err
            }
            res.send(JSON.stringify(rows))
            db.close()
        })
    })
})

app.get('/api/segments', function(req, res) {
    let db = dbConnect()
    let graphicName = req.query.name
    if (!graphicName) {
        var sql = `SELECT name FROM segmentdisp ORDER BY id`
    } else {
        var sql = `SELECT * FROM segmentdisp WHERE name = '` + graphicName + `' LIMIT 1`
    }
    res.setHeader('Content-Type', 'application/json')
    db.all(sql, [], (err, rows) => {
        if (err) {
            throw err
        }
        res.send(JSON.stringify(rows))
        db.close()
    })
})

app.post('/api/segments/update', function(req, res) {
    let db = dbConnect()
    let data = JSON.parse(req.body.data)
    let entries = data.length
    if (data.id == 999999) {
        var sql3 = `INSERT INTO segmentdisp(name,data) VALUES (?,?);`
        var values = [data.name, JSON.stringify(data.data)]
    } else {
        var sql3 = `UPDATE segmentdisp SET name=?, data=? WHERE id=?`
        var values = [data.name, JSON.stringify(data.data), data.id]
    }

    db.run(sql3, values, function(err) {
        if (err) {
            return console.error(err.message);
        }
    })

    var sql = `SELECT name FROM segmentdisp ORDER BY id`
    db.all(sql, [], (err, rows) => {
        if (err) {
            throw err
        }
        res.setHeader('Content-Type', 'application/json')
        res.send(JSON.stringify(rows))
        db.close()
    })
})

var port = process.env.PORT || 2600
app.listen(port, function() {
    console.log("Server Up. Listening on Port: " + port)
})