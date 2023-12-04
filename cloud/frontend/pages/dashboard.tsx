// import Das from "@components/Des"
import ApplicationDashboard from "@components/Dashboard";
import PrivateRoute from "@components/PrivateRoute";
import { useState } from "react";
import { useSession, useText } from "domain/layer"
import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

function createData(
  uuid: string,
  text: number,
  metadata: { source: string, timestamp: string},
) {
  const source = metadata.source;
  const timestamp = metadata.timestamp;
  return { uuid, timestamp, text, source };
}

// const rows = [
//   createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
//   createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
//   createData('Eclair', 262, 16.0, 24, 6.0),
//   createData('Cupcake', 305, 3.7, 67, 4.3),
//   createData('Gingerbread', 356, 16.0, 49, 3.9),
// ];

const Dashboard = () => {
  const session = useSession()
  const { getTexts } = useText()
  const [textoBusqueda, setTextoBusqueda] = useState('');
  const [rows, setRows] = useState([]);
  const handleTextoBusquedaChange = (e: any) => {
    setTextoBusqueda(e.target.value);
  };

  const handleBuscarClick = async () => {
    try{
      const { data } = await getTexts(textoBusqueda, 5)
      console.log("texts", data)
      const buildRows = data.map((item: any) => createData(item.uuid, item.text, item.metadata ));
      console.log(buildRows)
      setRows(buildRows)
    }
    catch(e){
      console.log(e)
      console.log('Buscar haciendo algo con:', textoBusqueda);
    }
  };

  return (
    <PrivateRoute>
      <div className="dashboard">
      <h1>{`Hola ${session.name}!`}</h1>
      <div className="busqueda">
        <input
          type="text"
          placeholder="Buscar..."
          value={textoBusqueda}
          onChange={handleTextoBusquedaChange}
        />
        <button onClick={handleBuscarClick}>Buscar</button>
        </div>
         <Slider
            style={{width: "10rem"}}
            defaultValue={5}
            min={1}
            max={10}
            valueLabelDisplay="auto"
          />
      </div>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell >TEXTO</TableCell>
                  <TableCell >TIMESTAMP</TableCell>
                  <TableCell >RECURSO</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row: any) => (
                  <TableRow
                    key={row.uuid}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell scope="row">
                      {row.text}
                    </TableCell>
                    <TableCell align="right">{row.timestamp}</TableCell>
                    <TableCell align="right">{row.source}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
    </PrivateRoute>
  )
}

export default Dashboard;
