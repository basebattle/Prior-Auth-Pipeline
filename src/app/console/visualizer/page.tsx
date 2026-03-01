import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { PipelineDisplay } from "@/components/dashboard/PipelineDisplay";
import { Suspense } from "react";

export default function VisualizerPage() {
    return (
        <DashboardLayout>
            <Suspense fallback={<div>Loading pipeline...</div>}>
                <PipelineDisplay />
            </Suspense>
        </DashboardLayout>
    );
}
