// import Das from "@components/Des"
import ApplicationDashboard from "@components/Dashboard";
import PrivateRoute from "@components/PrivateRoute";

const Dashboard = () => {
  return (
    <PrivateRoute>
      <div style={{color: "white"}}>hey user~</div>
    </PrivateRoute>
  )
}

export default Dashboard;
