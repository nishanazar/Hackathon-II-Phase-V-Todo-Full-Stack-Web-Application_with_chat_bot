'use client';

import { ReactNode, useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import FloatingChatWidget from './FloatingChatWidget';

type Props = {
  children: ReactNode;
};

const ConditionalFloatingChatProvider = ({ children }: Props) => {
  const pathname = usePathname();
  const [shouldShowChat, setShouldShowChat] = useState(false);

  useEffect(() => {
    // Define the pages where the chatbot should appear
    const showChatOnPaths = ['/dashboard', '/tasks'];

    // Check if current path is in the allowed paths
    const showChat = showChatOnPaths.some(path =>
      pathname === path || pathname.startsWith(`${path}/`)
    );

    setShouldShowChat(showChat);
  }, [pathname]);

  return (
    <>
      {children}
      {shouldShowChat && <FloatingChatWidget />}
    </>
  );
};

export default ConditionalFloatingChatProvider;