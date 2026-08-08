import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Login from './pages/Login';

const queryClient = new QueryClient();

export default function PathToGrad() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/student-dashboard" element={<div className="p-10">Welcome to your Dashboard!</div>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}