import Dashboard from "./pages/dashboard";

const MainLayout = () => {
    return ( 
        <div className="flex-col">
            <nav className="bg-gray-900 h-16 flex items-center justify-between px-6">
                <span className="text-white">Welcome, User</span>
            </nav>
            <Dashboard></Dashboard>
        </div>
     );
}
 
export default MainLayout;