import React from "react";
import "./globals.css";

export const metadata = {
  title: "MLCloudEngine — Enterprise Machine Learning Platform",
  description: "End-to-end Machine Learning Cloud Platform for Datasets, Training, Model Governance, Serving & Monitoring",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-dark-bg text-gray-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
