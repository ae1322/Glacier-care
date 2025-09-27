import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Heart } from "lucide-react";

interface AuthNavigationProps {
  currentPage: 'login' | 'signup';
}

const AuthNavigation: React.FC<AuthNavigationProps> = ({ currentPage }) => {
  return (
    <div className="flex items-center justify-between w-full max-w-md">
      <Link to="/" className="flex items-center gap-2 text-primary hover:opacity-80 transition-opacity">
        <Heart className="h-6 w-6" />
        <span className="text-lg font-semibold">HealthTranslate</span>
      </Link>
      
      <div className="flex gap-2">
        <Button
          variant={currentPage === 'login' ? 'default' : 'outline'}
          size="sm"
          asChild
        >
          <Link to="/login">Login</Link>
        </Button>
        <Button
          variant={currentPage === 'signup' ? 'default' : 'outline'}
          size="sm"
          asChild
        >
          <Link to="/signup">Signup</Link>
        </Button>
      </div>
    </div>
  );
};

export default AuthNavigation;
