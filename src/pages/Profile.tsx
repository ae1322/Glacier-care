import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { 
  User, 
  Mail, 
  Calendar, 
  Shield, 
  Settings, 
  Edit3, 
  Save, 
  X, 
  LogOut,
  Heart,
  FileText,
  Bell,
  Lock,
  Globe
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Profile = () => {
  const { user, logout } = useAuth();
  const { toast } = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
  });

  const handleEditToggle = () => {
    if (isEditing) {
      // Reset form to original values
      setEditForm({
        firstName: user?.firstName || '',
        lastName: user?.lastName || '',
        email: user?.email || '',
      });
    }
    setIsEditing(!isEditing);
  };

  const handleSave = async () => {
    // In a real app, you would call an API to update user profile
    toast({
      title: "Profile Updated",
      description: "Your profile has been successfully updated.",
    });
    setIsEditing(false);
  };

  const handleLogout = async () => {
    const result = await logout();
    if (result.success) {
      toast({
        title: "Logged Out",
        description: "You have been successfully logged out.",
      });
    } else {
      toast({
        title: "Error",
        description: result.error || "Failed to logout",
        variant: "destructive",
      });
    }
  };

  const getInitials = (firstName?: string, lastName?: string) => {
    const first = firstName?.charAt(0) || '';
    const last = lastName?.charAt(0) || '';
    return (first + last).toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || 'U';
  };

  const getDisplayName = () => {
    if (user?.firstName && user?.lastName) {
      return `${user.firstName} ${user.lastName}`;
    }
    return user?.displayName || user?.email || 'User';
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-background to-medical-light">
      {/* Header */}
      <header className="bg-card border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2 text-primary">
              <Heart className="h-6 w-6" />
              <span className="text-lg font-semibold">Glacier Care</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <User className="h-4 w-4" />
                <span>{user?.email}</span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                className="flex items-center gap-2"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Profile Header */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src="" alt={getDisplayName()} />
              <AvatarFallback className="text-2xl font-semibold bg-primary text-primary-foreground">
                {getInitials(user?.firstName, user?.lastName)}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 space-y-2">
              <h1 className="text-3xl font-bold text-foreground">{getDisplayName()}</h1>
              <p className="text-muted-foreground flex items-center gap-2">
                <Mail className="h-4 w-4" />
                {user?.email}
              </p>
              <div className="flex items-center gap-2">
                <Badge variant="secondary" className="flex items-center gap-1">
                  <Shield className="h-3 w-3" />
                  Verified Account
                </Badge>
                <Badge variant="outline" className="flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  Member since {new Date().getFullYear()}
                </Badge>
              </div>
            </div>
            <Button
              onClick={handleEditToggle}
              variant={isEditing ? "outline" : "default"}
              className="flex items-center gap-2"
            >
              {isEditing ? (
                <>
                  <X className="h-4 w-4" />
                  Cancel
                </>
              ) : (
                <>
                  <Edit3 className="h-4 w-4" />
                  Edit Profile
                </>
              )}
            </Button>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {/* Personal Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5" />
                  Personal Information
                </CardTitle>
                <CardDescription>
                  Your basic profile information
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {isEditing ? (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="firstName">First Name</Label>
                        <Input
                          id="firstName"
                          value={editForm.firstName}
                          onChange={(e) => setEditForm(prev => ({ ...prev, firstName: e.target.value }))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="lastName">Last Name</Label>
                        <Input
                          id="lastName"
                          value={editForm.lastName}
                          onChange={(e) => setEditForm(prev => ({ ...prev, lastName: e.target.value }))}
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        value={editForm.email}
                        onChange={(e) => setEditForm(prev => ({ ...prev, email: e.target.value }))}
                        disabled
                      />
                      <p className="text-xs text-muted-foreground">
                        Email cannot be changed
                      </p>
                    </div>
                    <Button onClick={handleSave} className="w-full flex items-center gap-2">
                      <Save className="h-4 w-4" />
                      Save Changes
                    </Button>
                  </>
                ) : (
                  <>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-sm font-medium text-muted-foreground">First Name</span>
                        <span className="text-sm">{user?.firstName || 'Not provided'}</span>
                      </div>
                      <Separator />
                      <div className="flex justify-between">
                        <span className="text-sm font-medium text-muted-foreground">Last Name</span>
                        <span className="text-sm">{user?.lastName || 'Not provided'}</span>
                      </div>
                      <Separator />
                      <div className="flex justify-between">
                        <span className="text-sm font-medium text-muted-foreground">Email</span>
                        <span className="text-sm">{user?.email}</span>
                      </div>
                      <Separator />
                      <div className="flex justify-between">
                        <span className="text-sm font-medium text-muted-foreground">User ID</span>
                        <span className="text-sm font-mono text-xs">{user?.uid}</span>
                      </div>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>

            {/* Account Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Account Settings
                </CardTitle>
                <CardDescription>
                  Manage your account preferences
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Bell className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <p className="text-sm font-medium">Email Notifications</p>
                        <p className="text-xs text-muted-foreground">Receive updates about your reports</p>
                      </div>
                    </div>
                    <Badge variant="secondary">Enabled</Badge>
                  </div>
                  <Separator />
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Lock className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <p className="text-sm font-medium">Two-Factor Authentication</p>
                        <p className="text-xs text-muted-foreground">Add extra security to your account</p>
                      </div>
                    </div>
                    <Badge variant="outline">Disabled</Badge>
                  </div>
                  <Separator />
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Globe className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <p className="text-sm font-medium">Language</p>
                        <p className="text-xs text-muted-foreground">Interface language</p>
                      </div>
                    </div>
                    <Badge variant="outline">English</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Usage Statistics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Usage Statistics
                </CardTitle>
                <CardDescription>
                  Your activity on Glacier Care
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-muted-foreground">Reports Analyzed</span>
                    <span className="text-sm font-semibold">0</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-muted-foreground">Account Created</span>
                    <span className="text-sm">{new Date().toLocaleDateString()}</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-muted-foreground">Last Active</span>
                    <span className="text-sm">Just now</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Security & Privacy */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Security & Privacy
                </CardTitle>
                <CardDescription>
                  Your data protection and privacy settings
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium">Data Encryption</p>
                      <p className="text-xs text-muted-foreground">All your data is encrypted</p>
                    </div>
                    <Badge variant="secondary" className="bg-green-100 text-green-800">
                      <Shield className="h-3 w-3 mr-1" />
                      Protected
                    </Badge>
                  </div>
                  <Separator />
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium">HIPAA Compliance</p>
                      <p className="text-xs text-muted-foreground">Healthcare data protection</p>
                    </div>
                    <Badge variant="secondary" className="bg-green-100 text-green-800">
                      <Shield className="h-3 w-3 mr-1" />
                      Compliant
                    </Badge>
                  </div>
                  <Separator />
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium">Data Retention</p>
                      <p className="text-xs text-muted-foreground">Reports stored for 1 year</p>
                    </div>
                    <Badge variant="outline">1 Year</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>
                Common tasks and account management
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                  <Settings className="h-6 w-6" />
                  <span className="text-sm">Account Settings</span>
                </Button>
                <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                  <Lock className="h-6 w-6" />
                  <span className="text-sm">Change Password</span>
                </Button>
                <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                  <FileText className="h-6 w-6" />
                  <span className="text-sm">Download Data</span>
                </Button>
                <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2 text-destructive hover:text-destructive">
                  <LogOut className="h-6 w-6" />
                  <span className="text-sm">Delete Account</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
};

export default Profile;
