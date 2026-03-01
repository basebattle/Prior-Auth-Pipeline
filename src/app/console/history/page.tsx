import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { HistoryTable } from "@/components/dashboard/HistoryTable";

export default function HistoryPage() {
    return (
        <DashboardLayout>
            <HistoryTable />
        </DashboardLayout>
    );
}
