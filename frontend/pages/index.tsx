export const metadata = {
  title: 'Home - Open PRO',
  description: 'Page description',
}
import PrivateRoute from "@components/PrivateRoute"

// import Hero from '@components/LandingPage/hero'
// import Features from '@components/LandingPage/features'
// import Newsletter from '@components/LandingPage/newsletter'
// import Zigzag from '@components/LandingPage/zigzag'
// import Testimonials from '@components/LandingPage/testimonials'
// import DefaultLayout from 'layouts/index'
// import RootLayout from 'layouts/layout'

export default function Home() {
  return (
    <PrivateRoute>
      <div style={{color: "white"}}>
        Not logged yet
      </div>
    </PrivateRoute>
    // <RootLayout>
    //   <DefaultLayout>
    //     <Hero />
    //     {/* <Features /> */}
    //     <Zigzag />
    //     {/* <Testimonials /> */}
    //     {/* <Newsletter /> */}
    //   </DefaultLayout>
    // </RootLayout>
  )
}
