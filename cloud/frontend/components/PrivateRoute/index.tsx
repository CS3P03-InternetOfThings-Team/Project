
import { useSession } from "domain/layer"
import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}
export default function PrivateRoute ({
  children,
}: Props){
  const session = useSession()
  if(!session) window.location.href = "/signin"
  else{
    return (
      <>
        {children}
      </>
    )
  }
}
