// Root layout for the app that doesn't include the floating chat widget
// The floating chat widget will be added in specific sections only
export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {children}
    </>
  );
}