import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { RequestForm } from "@/components/dashboard/RequestForm";

export default function NewRequestPage() {
    return (
        <DashboardLayout>
            <RequestForm />
        </DashboardLayout>
    );
}
