const {FILE} = require('dns');
const express = require('express');
const app = express();
const os = require('os')
const path = require('path');
const port = 3000;
const sqlite3 = require('sqlite3').verbose();
const multer = require('multer')
const bodyParser = require('body-parser')


const ABS_SCRIPT_PATH = path.resolve(__dirname);
const parentDir = path.join(ABS_SCRIPT_PATH, '..');

const DDBB_FOLDER_NAME = process.env.DATABASE_FOLDER_NAME;
const ELEMENT_DB_FILENAME = process.env.ELEMENT_DB_FILENAME;
const TABLELIST_DB_FILENAME = process.env.TABLELIST_DB_FILENAME;
const ORDER_DB_FILENAME = process.env.ORDER_DB_FILENAME;
const IMAGE_FOLDER_NAME = process.env.IMAGE_FOLDER_NAME;


const FILE_PATH = [
    path.join(parentDir,DDBB_FOLDER_NAME,ELEMENT_DB_FILENAME),
    path.join(parentDir,DDBB_FOLDER_NAME, TABLELIST_DB_FILENAME),
    path.join(parentDir,DDBB_FOLDER_NAME,ORDER_DB_FILENAME),
    path.join(parentDir,IMAGE_FOLDER_NAME)

];

app.get('/',(req,res) =>{
    res.send('Hello, World!')
})

app.get('/api/Elementos',(req,res)=>{
    const db = new sqlite3.Database(FILE_PATH[0]);
    const sqlQuery = 'SELECT * FROM Elementos';
    db.all(sqlQuery,(err,rows) =>{
        if(err){
            console.error('Error:',err.message);
            return;
        }else{

            res.json(rows);
        }

        db.close()

    })
})

app.get('/download/:imageName', (req,res) =>{
    const imageName = req.params.imageName;
    const filename = 'Imagenes';
    const currentPath = path.resolve(__dirname , '..');
    const filePath = path.join(currentPath, filename,imageName);
    res.sendFile(filePath,filename, (err) =>{

        if(err){
            console.error('Error downloading file:',err);

        }else{
            console.log('File downloaded successfully')
        }

    })

});

app.use(bodyParser.json())

app.post('/api/Pedidos',(req,res)=>{

    const NumeroMesa = req.body[0]["NumeroMesa"];
    const db = new sqlite3.Database(FILE_PATH[2]);
    const DataBase = `PedidosAuxiliares${NumeroMesa}`
    const sqlQuery = `SELECT * FROM ${DataBase}`;
    db.all(sqlQuery,(err,rows) =>{
        if(err){
            console.error('Error:',err.message);
            return;
        }else{
        res.json(rows);
        }
        db.close()

    })


})

app.get('/api/Mesas',(req,res)=>{
    console.log(FILE_PATH[1])

    const db = new sqlite3.Database(FILE_PATH[1]);
    const sqlQuery = 'SELECT * FROM ListaDeMesas';
    db.all(sqlQuery,(err,rows) =>{
        if(err){
            console.error('Error:',err.message);
            return;
        }else{
        res.json(rows);
        }

        db.close()

    })

})

app.get('/api/updateElemento', (req, res) => {
   const {NombreProducto, PrecioProducto, ImagenDireccion} = req.query;
    const db = new sqlite3.Database(FILE_PATH[0]);
    const sqlQuery = "INSERT INTO Elementos (NombreProducto, PrecioProducto, ImagenDireccion) VALUES (?, ?, ?)";

    db.all(sqlQuery,[NombreProducto,PrecioProducto, ImagenDireccion],(err,rows) =>{
        if(err){
            console.error('Error:',err.message);
        }else{
            res.send("Received")
        }

        db.close()

    })

});


app.get('/api/editElemento', (req, res) => {
    const {NombrePrevio,NombreProducto, PrecioProducto, ImagenDireccion} = req.query;
     const db = new sqlite3.Database(FILE_PATH[0]);
     const sqlQuery = "UPDATE Elementos SET NombreProducto = ?, PrecioProducto = ?, ImagenDireccion = ? WHERE NombreProducto = ?";
 
     db.all(sqlQuery,[NombreProducto,PrecioProducto, ImagenDireccion,NombrePrevio],(err) =>{
         if(err){
             console.error('Error:',err.message);
         }else{
             res.send("Received")
         }
         db.close()
 
     })
 
 });

app.get('/api/editPedido', (req,res) =>{

    const {NombrePrevio,NumeroMesa,NombreProducto,PrecioProducto,CantidadProducto,ImagenDireccion,NotasProducto} = req.query;
    const db = new sqlite3.Database(FILE_PATH[2]);
    console.log(FILE_PATH[2]);
    console.log(NombrePrevio,NumeroMesa,NombreProducto,PrecioProducto,CantidadProducto,ImagenDireccion,NotasProducto);
    const DataBaseName = `PedidosAuxiliares${NumeroMesa}`
    const sqlQuery = `UPDATE "${DataBaseName}" SET NombreProducto = ?, PrecioProducto = ?, CantidadProducto = ?, ImagenDireccion = ?, NotasProducto = ? WHERE NombreProducto = ?`;

    db.all(sqlQuery,[NombreProducto,PrecioProducto,CantidadProducto,ImagenDireccion,NotasProducto,NombrePrevio], (err) =>{

        if(err){
            console.error('Error:',err.message);
        }else{
            res.send("Received")
        }
        db.close();

    })

 })


 app.get('/api/addPedido', (req,res) =>{

    const {NumeroMesa,NombreProducto,PrecioProducto,CantidadProducto,ImagenDireccion,NotasProducto} = req.query;
    const db = new sqlite3.Database(FILE_PATH[2]);
    console.log(FILE_PATH[2]);
    console.log(NumeroMesa,NombreProducto,PrecioProducto,CantidadProducto,ImagenDireccion,NotasProducto);
    const DataBaseName = `PedidosAuxiliares${NumeroMesa}`
    const sqlQuery = `INSERT INTO "${DataBaseName}" (NombreProducto, PrecioProducto, CantidadProducto, ImagenDireccion, NotasProducto)
    VALUES(?,?,?,?,?)
    `;
    db.all(sqlQuery,[NombreProducto,PrecioProducto,CantidadProducto,ImagenDireccion,NotasProducto], (err) =>{

        if(err){
            console.error('Error:',err.message);
        }else{
            res.send("Received")
        }
        db.close();

    })

 })

 app.get('/api/deleteElemento',(req,res) =>{

    const {NombreEliminar} = req.query;
    console.log(NombreEliminar)
    const db = new sqlite3.Database(FILE_PATH[0]);
     const sqlQuery = "DELETE FROM Elementos WHERE NombreProducto LIKE ?";
     db.all(sqlQuery,[NombreEliminar],(err) =>{
         if(err){
             console.error('Error:',err.message);
         }else{
             res.send("Received")
         }
         db.close()
 
     })

 })

 app.get('/api/deleteAllElementos',(req,res)=>{
    const db = new sqlite3.Database(FILE_PATH[0]);
     const sqlQuery = "DELETE FROM Elementos";
     db.all(sqlQuery,(err) =>{
         if(err){
             console.error('Error:',err.message);
         }else{
             res.send("Received")
         }
         db.close()
 
     })

 })


 app.get('/api/deleteMesa', (req, res) => {
    const {NumeroMesa} = req.query; // Assuming NumeroMesa is a property of the request body
    const db = new sqlite3.Database(FILE_PATH[1]);

    const sqlQuery = "DELETE FROM ListaDeMesas WHERE NumeroMesa = ?";
    db.run(sqlQuery, [NumeroMesa], (err) => {
        if (err) {
            console.error('Error:', err.message);
            res.status(500).send('Error occurred while deleting the mesa.');
        } else {
            console.log(`Deleted mesa with NumeroMesa${NumeroMesa}`);
            // Close the database connection when the operation is done
            db.close();
            
            // Now, proceed to delete the corresponding auxiliary table
            const db2 = new sqlite3.Database(FILE_PATH[2]);
            const databaseName = `PedidosAuxiliares${NumeroMesa}`; // Use backticks for string interpolation
            const sqlQuery2 = `DROP TABLE IF EXISTS ${databaseName}`;
            
            db2.run(sqlQuery2,(err2) => {
                if (err2) {
                    console.error('Error:', err2.message);
                    res.status(500).send('Error occurred while deleting the auxiliary table.');
                }else{
                    console.log(`Deleted auxiliary table ${databaseName}`);
                    // Close the second database connection when the operation is done
                    db2.close();
                    res.send("Received");
                }
            });
        }
    });
});

 app.get('/api/deleteAllMesa',(req,res) =>{

    const db = new sqlite3.Database(FILE_PATH[1]);
     const sqlQuery = "DELETE FROM ListaDeMesas";
     db.all(sqlQuery,(err) =>{
         if(err){
             console.error('Error:',err.message);
         }else{
             res.send("Received")
         }
         db.close()
 
     })

     const tableToKeep = "PedidosAuxiliares"

    const db2 = new sqlite3.Database(FILE_PATH[2]);
    db.serialize(() => {
        db.all("SELECT name FROM sqlite_master WHERE type='table'", (err, tables) => {
          if (err) {
            console.error(err.message);
            return;
          }
      
          // Step 3: Generate and execute DROP TABLE statements
          tables.forEach(table => {
            const tableName = table.name;
            if (tableName !== tableToKeep) {
              const dropTableQuery = `DROP TABLE IF EXISTS ${tableName}`;
              db.run(dropTableQuery, (err) => {
                if (err) {
                  console.error(`Error dropping table ${tableName}: ${err.message}`);
                } else {
                  console.log(`Dropped table ${tableName}`);
                }
              });
            }
          });
        });
      });

      db.close((err) => {
        if (err) {
          console.error(err.message);
        } else {
          console.log('Database connection closed.');
        }
    })
 })


 app.get('/api/deletePedido', (req, res) => {
    const { NumeroMesa, NombreProducto } = req.query; // Assuming NumeroMesa and NombreProducto are properties of the request body
    const db = new sqlite3.Database(FILE_PATH[2]);
    const DataBaseName = `PedidosAuxiliares${NumeroMesa}`; // Use backticks for string interpolation

    const sqlQuery = `DELETE FROM ${DataBaseName} WHERE NombreProducto LIKE ?`;
    db.run(sqlQuery, [NombreProducto], (err) => {
        if (err) {
            console.error('Error:', err.message);
            res.status(500).send('Error occurred while deleting the pedido.');
        } else {
            console.log(`Deleted pedido with NombreProducto ${NombreProducto} from ${DataBaseName}`);
            // Close the database connection when the operation is done
            db.close();
            res.send("Received");
        }
    });
});

// Configure multer storage
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null,FILE_PATH[3]); // Set the destination folder for uploaded images
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname); // Use the original filename for uploaded images
    },
});

const upload = multer({ storage: storage });

app.post('/upload/images', upload.single('imagen'), (req, res) => {
    if (!req.file) {
        
        res.status(404).send("No image was provided")
    }
    
    res.status(200).send("Image Provided");
    
});

app.use(bodyParser.json())

app.post('/upload/Pedidos', (req, res) => {
    const json_data = req.body;

    // Connect to the database for creating the table
    const db = new sqlite3.Database(FILE_PATH[2]);
    const NuevaBase = `PedidosAuxiliares${json_data[0]["id"]}`;
    const sqlQuery = `
        CREATE TABLE IF NOT EXISTS ${NuevaBase} (
            NombreProducto TEXT,
            PrecioProducto FLOAT,
            ImagenDireccion TEXT,
            CantidadProducto INTEGER,
            NotasProducto TEXT
        )
    `;

    db.run(sqlQuery, (err) => {
        if (err) {
            console.error('Error creating table:', err.message);
            res.status(500).send('Error creating table');
        } else {
            // Insert data into the table
            const sqlQuery2 = `
                INSERT INTO ${NuevaBase} (NombreProducto, PrecioProducto, ImagenDireccion, CantidadProducto, NotasProducto)
                VALUES (?, ?, ?, ?, ?)
            `;

            for (let i = 1; i < json_data.length; i++) {
                const values = [
                    json_data[i]["NombreProducto"],
                    json_data[i]["PrecioProducto"],
                    json_data[i]["ImagenDireccion"],
                    json_data[i]["CantidadProducto"],
                    json_data[i]["NotasProducto"]
                ];

                db.run(sqlQuery2, values, (err) => {
                    if (err) {
                        console.error('Error:', err.message);
                        res.status(500).send('Error inserting data');
                    }
                });
            }

            // Close the database connection
            db.close();

            // Insert data into the "ListaDeMesas" table
            const db2 = new sqlite3.Database(FILE_PATH[1]);
            const sqlQuery3 = `
                INSERT INTO ListaDeMesas (NumeroMesa, NameOfAnotherDataBase)
                VALUES (?, ?)
            `;

            db2.run(sqlQuery3, json_data[0]["id"], NuevaBase, (err) => {
                if (err) {
                    console.error('Error:', err.message);
                    res.status(500).send('Error inserting data');
                } else {
                    // Close the second database connection
                    db2.close();

                    // Send the response once all data has been inserted
                    res.send('Received');
                }
            });
        }
    });
});



app.listen(port, () =>{
    console.log(`Server is running on port ${port}`);

})