import { Navigate } from "react-router-dom";
import { isAdmin } from "../utils/auth";

const AdminRoute = ({ children }) => {
  if (!isAdmin()) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

export default AdminRoute;
