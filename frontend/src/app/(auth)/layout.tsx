// This layout ensures that the floating chat widget does not appear on auth pages
export default function AuthLayout({
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