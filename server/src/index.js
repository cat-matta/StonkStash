const express = require('express');
const app = express();
const routes = require("./controllers");
const PORT = 8000;

//const db = require("./config/keys").mongoURI;



app.use(express.json()) // for parsing application/json
app.use(express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

app.use('/api', routes);


app.listen(PORT, () =>
  console.log(`StonkStache-1 Backend listening on port ${PORT}!`)
);