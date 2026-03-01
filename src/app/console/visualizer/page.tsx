import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { PipelineDisplay } from "@/components/dashboard/PipelineDisplay";

export default function VisualizerPage() {
    return (
        <DashboardLayout>
            <PipelineDisplay />
        </DashboardLayout>
    );
}
