import * as express from "express"
import * as path from "path"
import * as fs from "fs"

const app = express.default()
const port = 7272

app.use(express.static(path.join(__dirname, "..")))
app.use(express.static(path.join(__dirname, '..', 'static')))

// Path debugging helper 
app.get('*', (req, res) => {
    const fullPath = path.join(__dirname, req.path)
    const dir = fs.opendirSync(fullPath)
    let entity
    let listing = []
    while((entity = dir.readSync()) !== null) {
        if(entity.isFile()) {
            listing.push({ type: 'f', name: entity.name })
        } else if(entity.isDirectory()) {
            listing.push({ type: 'd', name: entity.name })
        }
    }
    dir.closeSync()
    res.send(listing)
})

app.listen(
    port, 
    () => console.log("Succesfully started server")
)
